"""Transaction between two parties: data, hash and dictionary representation.

Public entry point: run(fields). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import hashlib
from dataclasses import dataclass, asdict


@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float
    timestamp: str

    def __post_init__(self):
        self.public_key = None
        self.signature = None

    @property
    def hash(self):
        return hashlib.sha256((str(self.sender) + str(self.receiver) + str(self.amount) + str(self.timestamp)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return asdict(self)


def run(fields):
    """Public entry point of this unit.

    fields: sender, receiver, amount and timestamp. Returns the dictionary
    representation of the transaction.
    """
    transaction = Transaction(fields["sender"], fields["receiver"], fields["amount"], fields["timestamp"])
    return transaction.repr_json()
