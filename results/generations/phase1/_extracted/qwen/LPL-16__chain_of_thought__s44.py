"""Transaction between two parties: data, hash and dictionary representation.

Public entry point: run(fields). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import hashlib


class TransactionParams:
    def __init__(self, sender, receiver, amount, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp


class Transaction(object):
    def __init__(self, params):
        self.sender = params.sender
        self.receiver = params.receiver
        self.amount = params.amount
        self.timestamp = params.timestamp
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


def run(params):
    """Public entry point of this unit.

    params: An instance of TransactionParams.
    Returns the dictionary representation of the transaction.
    """
    transaction = Transaction(params)
    return transaction.repr_json()
