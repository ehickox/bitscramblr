import os
import sys
import blockchain
import coinbase
import random
from blockchain.wallet import Wallet as BlockchainWallet
from coinbase.client import Client as CoinbaseClient
from models import Node, Tx
from app import db, logger

blockchain = None
bc_primary = os.environ['BLOCKCHAIN_PRIMARY']
bc_secondary = os.environ['BLOCKCHAIN_SECONDARY']

if bc_primary is not None and bc_secondary is not None:
    blockchain = BlockchainWallet(bc_primary,bc_secondary)
                                    
THRESHOLD_RECEIVERS = 2
THRESHOLD_SHUFFLERS = 1
MAX_BLUNDERBUSS = 5

def generate_receiver(destination, pending_amt):
    """
    Generates a new receiving address and adds a pending transaction to db

    :return: str the address generated
    """
    bc_address = blockchain.new_address(label="RECEIVING")
    node = Node(address=bc_address.address, role="receiving", status='pending',
                        balance=bc_address.balance, destination=destination,
                        pending_amt=pending_amt, label="RECEIVING")
    tx = Tx(parent=bc_address.address, amount=pending_amt, destination=destination)

    db.session.add(tx)
    db.session.add(node)
    db.session.commit()
    return bc_address.address
    
def blunderbuss(parent, amount):
    """
    Generates a random number of addresses between 1 and MAX_BLUNDERBUSS,
    then distributes the proportion randomly among them.
    
    TODO: proportions are currently even. make them random.

    :param str parent: the address of the parent
    :param float amount: the amount to be distributed over the generated shufflers
    :return: true if success, false otherwise
    """
    success = True
    num_to_use = random.randint(1, MAX_BLUNDERBUSS)
    addresses_to_use = []
    nodes = []

    amount = amount - 0.0001 # account for miner's fee
    #percent_left = range(100)
        
    logger.info("generating "+str(num_to_use)+" shuffling addresses")

    # Generate new addresses and save them to db
    for i in range(num_to_use):
        try:
            bc_address = blockchain.new_address(label="SHUFFLING")
            addresses_to_use.append(bc_address.address)
            node = Node(address=bc_address.address, role="shuffling", status="fresh",
                                balance=bc_address.balance, parent=parent, label="SHUFFLING")
            db.session.add(node)
            db.session.commit()
            logger.info("saved shuffling address "+str(bc_address.address)+" to db")
        except Exception, error:
            success = False
            logger.error("error while generating shufflers")
            logger.error(error)

    recipients = {} # {'address':amount}
    # Package addresses and amounts into a dict to be sent in a single transaction
    for address in addresses_to_use:
        #amt_to_send = float(float(amount) * (float(perc_to_use) * 0.01))
        amt_to_send = float(1.0/float(num_to_use))*float(amount)
        satoshis = int(amt_to_send * float(100000000))
        # Send BTC from the receiving addr to the shuffling addresses
        recipients[address] = satoshis
        logger.info("packaging "+str(address)+" with "+str(amt_to_send))
        

    # Send the muti-address transaction to the shufflers.
    try:
        resp = blockchain.send_many(recipients=recipients, from_address=parent)
        logger.info(resp.message)
        logger.info(resp.tx_hash)
        for addr, amt in recipients.items():
            node = db.session.query(Node).filter(Node.address==addr).one()
            # DO NOT UPDATE BALANCE HERE
            db.session.commit()
    except Exception, error:
        success = False
        logger.error(error)
        
    return success

def focus_cloud(destination, amount, exclude_parents=[]):
    """
    Sends BTC to the provided destination from shufflers whose
    parent and origin are not in exclude_parents.
    :param str destination: the destination of the assembled transaction
    :param float amount: the amount to assemble into a transaction
    :param str list exclude_parent: list of parents and origins to exclude
    """

    success = True
    total_in_cluster = 0
    # Get a list of safe shufflers ordered by balance descending
    safe_shufflers_by_balance = db.session.query(Node).filter(
        ~Node.parent.in_(exclude_parents),
        ~Node.origin.in_(exclude_parents),
        ~Node.status.in_(['residual']),
        Node.balance > 0.0001,
        Node.role == 'shuffling').order_by(Node.balance.desc()).all()

    # Check to make sure there is enough BTC in the cloud
    for shuffler in safe_shufflers_by_balance:
        total_in_cluster += shuffler.balance

    if total_in_cluster < amount:
        logger.warning("not enough in cloud to complete tx!")
        success = False
        return success

    amount_left = amount
    for shuffler in safe_shufflers_by_balance:
        if shuffler.balance >= (amount_left + 0.0001): #miner's fee
            try:
                satoshis = int(float(amount_left) * float(100000000))
                resp = blockchain.send(to=destination, amount=satoshis, from_address=shuffler.address)
                logger.info(resp.message)
                shuffler.balance = shuffler.balance - amount_left
                shuffler.used = True
                shuffler.status = 'dormant'
                db.session.commit()
                amount_left -= amount_left
            except Exception, error:
                success = False
                logger.error(error)
                
        elif shuffler.balance < (amount_left + 0.0001) and shuffler.balance > 0.0002:
            try:
                satoshis = int(float(shuffler.balance-(10000/float(100000000))) * float(100000000))
                resp = blockchain.send(to=destination, amount=satoshis, from_address=shuffler.address)
                logger.info(resp.message)
                shuffler.balance = shuffler.balance - shuffler.balance
                shuffler.used = True
                shuffler.status = 'dormant'
                db.session.commit()
                amount_left -= shuffler.balance - (10000/float(100000000)) #account for fee
            except Exception, error:
                success = False
                logger.error(error)
                
        else:
            # Shuffler only has residuals left
            shuffler.used = True
            shuffler.status = 'residual'
            db.session.commit()

    return success


def clear_all(destination):
    """
    Sends all addresses balances to the specified destination
    """
    bc_addresses = blockchain.list_addresses(confirmations=2)
    for address in bc_addresses:
        if address.balance > 50000:
            amt = address.balance - 10000
            blockchain.send(to=destination, amount=amt, from_address=address.address)

def get_num_transactions():
    """
    Gets the current number of successfully made transactions
    """
    txs_made = db.session.query(Tx).filter(Tx.received_inputs==True,
                                           Tx.outputs_sent==True).all()
    return len(txs_made)

def get_swarm_size():
    """
    Gets the current size of all available fragments.
    This is the amount in BTC that could be instantly sent if a transaction
    was made at or below this amount.
    """
    amount = 0.0
    nodes = db.session.query(Node).filter(Node.role=="shuffling").all()

    for node in nodes:
        amount += node.balance

    return amount
        
