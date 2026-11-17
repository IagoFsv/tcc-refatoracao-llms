"""Transaction between two parties: data, hash and dictionary representation.

Public entry point: run(fields). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import hashlib
from dataclasses import dataclass

@dataclass
class TransactionData:
    sender: str
    receiver: str
    amount: float
    timestamp: float

class Transaction(object):
    def __init__(self, data: TransactionData):
        self.sender = data.sender
        self.receiver = data.receiver
        self.amount = data.amount
        self.timestamp = data.timestamp
        self.public_key = None
        self.signature = None

    @property
    def hash(self):
        return hashlib.sha256((str(self.sender) + str(self.receiver) + str(self.amount) + str(self.timestamp)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "hash": self.hash
        }

def run(fields):
    """Public entry point of this unit.

    fields: dictionary containing sender, receiver, amount and timestamp. Returns the dictionary
    representation of the transaction.
    """
    data = TransactionData(**fields)
    transaction = Transaction(data)
    return transaction.repr_json()
