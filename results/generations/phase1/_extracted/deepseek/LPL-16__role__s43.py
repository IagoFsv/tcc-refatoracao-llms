"""Transaction between two parties: data, hash and dictionary representation.

Public entry point: run(fields). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import hashlib


class Params(object):
    def __init__(self, sender, receiver, amount, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp


class Transaction(object):
    def __init__(self, params, *args, **kwargs):
        self.params = params
        self.public_key = None
        self.signature = None

    @property
    def hash(self):
        return hashlib.sha256((str(self.params.sender) + str(self.params.receiver) + str(self.params.amount) + str(self.params.timestamp)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return {
            "sender": self.params.sender,
            "receiver": self.params.receiver,
            "amount": self.params.amount,
            "timestamp": self.params.timestamp,
            "hash": self.hash
        }


def run(fields):
    """Public entry point of this unit.

    fields: sender, receiver, amount and timestamp. Returns the dictionary
    representation of the transaction.
    """
    params = Params(fields["sender"], fields["receiver"], fields["amount"], fields["timestamp"])
    transaction = Transaction(params)
    return transaction.repr_json()
