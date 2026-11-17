"""Block of a blockchain: data, hash and dictionary representation.

Public entry point: run(fields). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import hashlib


class _Transaction:
    """Minimal transaction, with only what the block uses: hash and repr_json."""

    def __init__(self, description):
        self.description = description

    @property
    def hash(self):
        return hashlib.sha256(self.description.encode('utf-8')).hexdigest()

    def repr_json(self):
        return {"description": self.description}


class BlockData:
    def __init__(self, index, timestamp, transactions, previous_hash, proof=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof


class Block(object):
    def __init__(self, block_data):
        self.index = block_data.index
        self.timestamp = block_data.timestamp
        self.transactions = block_data.transactions
        self.previous_hash = block_data.previous_hash
        self.proof = block_data.proof

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

    fields: a dictionary with the following keys: "index", "timestamp", "transactions" (descriptions), "previous_hash", and optionally, "proof". Returns the dictionary representation of the block.
    """
    block_data = BlockData(fields["index"], fields["timestamp"], [_Transaction(description) for description in fields["transactions"]], fields["previous_hash"])
    if "proof" in fields:
        block_data.proof = fields["proof"]
    block = Block(block_data)
    return block.repr_json()
