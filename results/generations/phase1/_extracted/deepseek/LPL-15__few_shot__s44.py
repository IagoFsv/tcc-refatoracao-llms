"""Block of a blockchain: data, hash and dictionary representation.

Public entry point: run(fields). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import hashlib
from dataclasses import dataclass, asdict


class Transaction:
    """Minimal transaction, with only what the block uses: hash and repr_json."""

    def __init__(self, description):
        self.description = description

    @property
    def hash(self):
        return hashlib.sha256(self.description.encode('utf-8')).hexdigest()

    def repr_json(self):
        return {"description": self.description}


@dataclass
class Block:
    index: int
    timestamp: str
    transactions: list
    previous_hash: str
    proof: str = None

    @property
    def hash(self):
        transactions_hash = "".join(list(map(lambda x: x.hash, self.transactions)))
        return hashlib.sha256((str(self.index) + str(self.timestamp) + transactions_hash + str(self.previous_hash) + str(self.proof)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return {
            "hash": self.hash,
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": list(map(lambda x: x.repr_json(), self.transactions)),
            "previous_hash": self.previous_hash,
            "proof": self.proof
        }


def run(fields):
    """Public entry point of this unit.

    fields: index, timestamp, transactions  (descriptions), previous_hash and,
    optionally, proof. Returns the dictionary representation of the block.
    """
    transactions = [Transaction(description) for description in fields["transactions"]]
    if "proof" in fields:
        block = Block(fields["index"], fields["timestamp"], transactions, fields["previous_hash"], fields["proof"])
    else:
        block = Block(fields["index"], fields["timestamp"], transactions, fields["previous_hash"])
    return asdict(block)
