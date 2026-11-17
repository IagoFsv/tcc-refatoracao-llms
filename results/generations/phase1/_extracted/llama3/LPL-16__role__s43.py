"""Transaction between two parties: data, hash and dictionary representation.

Public entry point: run(fields). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import hashlib


class TransactionData(object):
    def __init__(self, sender, receiver, amount, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp

    def __str__(self):
        return str(self.sender) + str(self.receiver) + str(self.amount) + str(self.timestamp)


class Transaction(object):
    def __init__(self, data):
        self.sender = data.sender
        self.receiver = data.receiver
        self.amount = data.amount
        self.timestamp = data.timestamp
        self.public_key = None
        self.signature = None

    @property
    def hash(self):
        return hashlib.sha256(self.__str__().encode('utf-8')).hexdigest()

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

    fields: dictionary with sender, receiver, amount and timestamp. Returns the dictionary
    representation of the transaction.
    """
    data = TransactionData(fields["sender"], fields["receiver"], fields["amount"], fields["timestamp"])
    transaction = Transaction(data)
    return transaction.repr_json()
