import hashlib

class _Transacao:
    def __init__(self, descricao):
        self.descricao = descricao

    @property
    def hash(self):
        return hashlib.sha256(self.descricao.encode('utf-8')).hexdigest()

    def repr_json(self):
        return {"descricao": self.descricao}


class Block(object):
    def __init__(self, block_data):
        self.index = block_data.index
        self.timestamp = block_data.timestamp
        self.transactions = [ _Transacao(transacao) for transacao in block_data.transactions ]
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


def executar(block_data):
    return Block(block_data).repr_json()
