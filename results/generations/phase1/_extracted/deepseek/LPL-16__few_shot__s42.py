"""Transaction between two parties: data, hash and dictionary representation.

Public entry point: run(fields). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import hashlib
from dataclasses import dataclass, asdict

@dataclass
class TransactionFields:
    sender: str
    receiver: str
    amount: float
    timestamp: str

@dataclass
class Transaction(object):
    def __init__(self, fields: TransactionFields, *args, **kwargs):
        self.fields = fields
        self.public_key = None
        self.signature = None

    @property
    def hash(self):
        return hashlib.sha256((str(self.fields.sender) + str(self.fields.receiver) + str(self.fields.amount) + str(self.fields.timestamp)).encode('utf-8')).hexdigest()

    def repr_json(self):
        fields_dict = asdict(self.fields)
        fields_dict["hash"] = self.hash
        return fields_dict


def run(fields):
    """Public entry point of this unit.

    fields: sender, receiver, amount and timestamp. Returns the dictionary
    representation of the transaction.
    """
    transaction_fields = TransactionFields(fields["sender"], fields["receiver"], fields["amount"], fields["timestamp"])
    transaction = Transaction(transaction_fields)
    return transaction.repr_json()
