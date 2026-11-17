"""Transaction between two parties: data, hash and dictionary representation.

Public entry point: run(fields). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import hashlib

class TransactionParams(object):
    def __init__(self, sender, receiver, amount, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp

class Transaction(object):
    def __init__(self, transaction_params, *args, **kwargs):
        self.transaction_params = transaction_params
        self.public_key = None
        self.signature = None

    @property
    def hash(self):
        return hashlib.sha256((str(self.transaction_params.sender) + str(self.transaction_params.receiver) + str(self.transaction_params.amount) + str(self.transaction_params.timestamp)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return {
            "sender": self.transaction_params.sender,
            "receiver": self.transaction_params.receiver,
            "amount": self.transaction_params.amount,
            "timestamp": self.transaction_params.timestamp,
            "hash": self.hash
        }


def run(fields):
    """Public entry point of this unit.

    fields: sender, receiver, amount and timestamp. Returns the dictionary
    representation of the transaction.
    """
    transaction_params = TransactionParams(fields["sender"], fields["receiver"], fields["amount"], fields["timestamp"])
    transaction = Transaction(transaction_params)
    return transaction.repr_json()
