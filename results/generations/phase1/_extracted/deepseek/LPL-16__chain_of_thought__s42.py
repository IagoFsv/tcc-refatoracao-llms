"""Transaction between two parties: data, hash and dictionary representation.

Public entry point: run(fields). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import hashlib


class TransactionFields(object):
    def __init__(self, sender, receiver, amount, timestamp, *args, **kwargs):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp


class Transaction(object):
    def __init__(self, transaction_fields: TransactionFields):
        self.sender = transaction_fields.sender
        self.receiver = transaction_fields.receiver
        self.amount = transaction_fields.amount
        self.timestamp = transaction_fields.timestamp
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

    fields: sender, receiver, amount and timestamp. Returns the dictionary
    representation of the transaction.
    """
    transaction_fields = TransactionFields(fields["sender"], fields["receiver"], fields["amount"], fields["timestamp"])
    transaction = Transaction(transaction_fields)
    return transaction.repr_json()
