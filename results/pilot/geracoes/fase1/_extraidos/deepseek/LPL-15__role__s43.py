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


class Block:
    def __init__(self, block_params):
        self.block_params = block_params

    @property
    def hash(self):
        params = self.block_params
        return hashlib.sha256((str(params.index) + str(params.timestamp) + "".join(list(map(lambda x: x.hash, params.transactions))) + str(params.previous_hash) + str(params.proof)).encode('utf-8')).hexdigest()

    def repr_json(self):
        params = self.block_params
        return {
            "hash": self.hash,
            "index": params.index,
            "timestamp": params.timestamp,
            "transactions": list(map(lambda x: x.repr_json(), params.transactions)),
            "previous_hash": params.previous_hash,
            "proof": params.proof
        }


def execute(fields):
    transactions = [Transaction(description) for description in fields["transactions"]]
    if "proof" in fields:
        block_params = BlockParams(fields["index"], fields["timestamp"], transactions, fields["previous_hash"], fields["proof"])
    else:
        block_params = BlockParams(fields["index"], fields["timestamp"], transactions, fields["previous_hash"])
    block = Block(block_params)
    return block.repr_json()
