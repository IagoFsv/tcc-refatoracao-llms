"""Block of a blockchain: data, hash and dictionary representation.

Public entry point: run(fields). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import hashlib


class Transaction:
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


class Block:
    def __init__(self, block_data):
        self.block_data = block_data

    @property
    def hash(self):
        transactions_hash = "".join(list(map(lambda x: x.hash, self.block_data.transactions)))
        return hashlib.sha256((str(self.block_data.index) + str(self.block_data.timestamp) + transactions_hash + str(self.block_data.previous_hash) + str(self.block_data.proof)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return {
            "hash": self.hash,
            "index": self.block_data.index,
            "timestamp": self.block_data.timestamp,
            "transactions": list(map(lambda x: x.repr_json(), self.block_data.transactions)),
            "previous_hash": self.block_data.previous_hash,
            "proof": self.block_data.proof
        }


def run(fields):
    """Public entry point of this unit.

    fields: index, timestamp, transactions  (descriptions), previous_hash and,
    optionally, proof. Returns the dictionary representation of the block.
    """
    transactions = [_Transaction(description) for description in fields["transactions"]]
    block_data = BlockData(fields["index"], fields["timestamp"], transactions, fields["previous_hash"], fields.get("proof"))
    block = Block(block_data)
    return block.repr_json()
