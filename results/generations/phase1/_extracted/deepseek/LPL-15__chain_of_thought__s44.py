import hashlib


class Transaction:
    def __init__(self, description):
        self.description = description

    @property
    def hash(self):
        return hashlib.sha256(self.description.encode('utf-8')).hexdigest()

    def repr_json(self):
        return {"description": self.description}


class BlockParams:
    def __init__(self, index, timestamp, transactions, previous_hash, proof=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof


class Block(object):
    def __init__(self, block_params: BlockParams):
        self.index = block_params.index
        self.timestamp = block_params.timestamp
        self.transactions = block_params.transactions
        self.previous_hash = block_params.previous_hash
        self.proof = block_params.proof if block_params.proof is not None else ""

    @property
    def hash(self):
        transactions_hash = "".join(list(map(lambda x: x.hash, self.transactions)))
        return hashlib.sha256((str(self.index) + str(self.timestamp) + transactions_hash +
                               str(self.previous_hash) + str(self.proof)).encode('utf-8')).hexdigest()

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
    transactions = [_Transaction(description) for description in fields["transactions"]]
    block_params = BlockParams(fields["index"], fields["timestamp"], transactions, fields["previous_hash"])
    if "proof" in fields:
        block_params.proof = fields["proof"]
    block = Block(block_params)
    return block.repr_json()
