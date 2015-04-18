import schedule
import time
import os
import controller
from app import db
from controller import logger, blockchain
from blockchain import blockexplorer
from models import Node, Tx

def update_balances():
    """
    Updates the balance of all addresses in db
    """
    logger.info("updating wallet balances")
    nodes = db.session.query(Node).all()
    bc_addresses = blockchain.list_addresses(confirmations=2)
    bc_addresses_by_addr = {}
    for bc_addr in bc_addresses:
        bc_addresses_by_addr[bc_addr.address] = {'balance':float(float(bc_addr.balance) / float(100000000))}

    for node in nodes:
        if node.address in bc_addresses_by_addr.keys():
            logger.info("updating balance of: "+str(node.address))
            node.balance = bc_addresses_by_addr[node.address]['balance']
            db.session.commit()
    
def update():
    """
    Checks/updates pending receiving addresses and checks/updates pending transactions
    """
    # Check all pending receivers
    pending_receivers = db.session.query(Node).filter(Node.role=='receiving',
                                                      Node.status=='pending').all()

    logger.info("pending receivers: "+str(len(pending_receivers)))
    for node in pending_receivers:
        # update the balance from bc.info
        logger.info("checking "+str(node.address))
        bc_address = blockchain.get_address(node.address, confirmations=2)

        node.balance = float(float(bc_address.balance) / float(100000000)) # satoshis -> BTC

        logger.info(str(node.address)+" has "+str(node.balance))
        
        if node.balance >= node.pending_amt:
            # get the origin of the receiver's balance
            origins = []
            node_bc_addr = blockexplorer.get_address(node.address)
            for tx in node_bc_addr.transactions:
                for inpt in tx.inputs:
                    logger.info("appending origin: "+str(inpt.address))
                    origins.append(inpt.address)

            if len(origins) > 1:
                logger.warn("change origin from db string to list!")

            origin_addr = origins[0]
            node.orign = origin_addr
                    
            # inputs have been received, so update its transaction and blunderbuss
            # tag wallet with the origin of its inputs
            tx = db.session.query(Tx).filter(Tx.parent==node.address).one()
            tx.received_inputs = True
            tx.origin = origin_addr
            blunderbussed = controller.blunderbuss(parent=node.address,amount=tx.amount)
            if blunderbussed:
                node.status='blunderbussed'
                logger.info("blunderbussed")
        db.session.commit()

    # Check all pending txs whose received inputs = True
    pending_txs = db.session.query(Tx).filter(Tx.received_inputs==True,
                                              Tx.outputs_sent==False).all()
    for tx in pending_txs:
        sent = controller.focus_cloud(destination=tx.destination,
                                      amount=tx.amount,
                                      exclude_parents=[tx.parent,tx.origin])
        if sent:
            tx.outputs_sent = True
            logger.info("tx sent")

        db.session.commit()

def archive_used_receivers():
    """
    Archives used (blunderbussed) receivers 
    """
    receivers = db.session.query(Node).filter(Node.role=='receiving',
                                              Node.status=='blunderbussed',
                                              Node.balance<Node.pending_amt)
    for receiver in receivers:
        logger.info("archiving used receiver: "+str(receiver.address))
        try:
            resp = blockchain.archive_address(receiver.address)
            logger.info("archived: "+str(resp))
            receiver.status = 'archived'
            db.session.commit()
        except Exception, error:
            logger.error(error)
        

def archive_residuals():
    """
    Archives any dormant/inactive/used address with a balance < miner's fee (0.0001)
    :return int: the number of addresses archived
    """
    pass
    

def clean():
    """
    Archives used/residual addresses and removes them from db
    """
    pass

    
if __name__ == "__main__":
    update_balances()
    #archive_used_receivers()
    update()
    update_balances()
        
