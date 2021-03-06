from app import db

class Node(db.Model):
    __tablename__ = 'nodes'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String)
    label = db.Column(db.String)
    role = db.Column(db.String)
    status = db.Column(db.String)
    balance = db.Column(db.Float)
    used = db.Column(db.Boolean)

    # Optional keys for receiving/shuffling wallets
    destination = db.Column(db.String)
    parent = db.Column(db.String)
    origin = db.Column(db.String)
    pending_amt = db.Column(db.Float)

    def __init__(self, address, role, status, balance, used=False,
                 destination=None, parent=None, origin=None,
                 pending_amt=None, label=None):
        self.address = address
        self.role = role
        self.balance = balance
        self.used = used
        self.status = status
        self.destination = destination
        self.parent = parent
        self.pending_amt = pending_amt
        self.label = label
        self.origin = origin

class Tx(db.Model):
    __tablename__ = 'txs'

    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.String)
    destination = db.Column(db.String)
    amount = db.Column(db.Float)
    received_inputs = db.Column(db.Boolean)
    outputs_sent = db.Column(db.Boolean)
    origin = db.Column(db.String)
    tx_hash = db.Column(db.String)

    def __init__(self, parent, amount,
                 destination, received_inputs=False, outputs_sent=False):
        self.parent = parent
        self.amount = amount
        self.destination = destination
        self.received_inputs = received_inputs
        self.outputs_sent = outputs_sent
