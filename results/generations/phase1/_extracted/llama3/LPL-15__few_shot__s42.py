"""Block of a blockchain: data, hash and dictionary representation.

Public entry point: run(fields). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import hashlib
from dataclasses import dataclass, asdict

@dataclass
class Transaction:
    description: str

    @property
    def hash(self):
        return hashlib.sha256(self.description.encode('utf-8')).hexdigest()

    def repr_json(self):
        return {"description": self.description}


@dataclass
class Block:
    index: int
    timestamp: str
    transactions: list[Transaction]
    previous_hash: str
    proof: str = None

    @property
    def hash(self):
        return hashlib.sha256((str(self.index) + str(self.timestamp) + "".join(list(map(lambda x: x.hash, self.transactions))) + str(self.previous_hash) + str(self.proof)).encode('utf-8')).hexdigest()

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

    fields: BlockData. Returns the dictionary representation of the block.
    """
    block_data = BlockData(**fields)
    return block_data.repr_json()


class BlockData:
    def __init__(self, index, timestamp, transactions, previous_hash, proof=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = [Transaction(description) for description in transactions]
        self.previous_hash = previous_hash
        self.proof = proof
