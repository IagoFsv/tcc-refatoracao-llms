import hashlib


class Transacao:
    def __init__(self, descricao):
        self.descricao = descricao

    @property
    def hash(self):
        return hashlib.sha256(self.descricao.encode('utf-8')).hexdigest()

    def repr_json(self):
        return {"descricao": self.descricao}


class BlockData:
    def __init__(self, index, timestamp, transactions, previous_hash, proof=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof


class Block(object):
    def __init__(self, block_data):
        self.block_data = block_data

    @property
    def hash(self):
        return hashlib.sha256((str(self.block_data.index) + str(self.block_data.timestamp) + "".join(list(map(lambda x: x.hash, self.block_data.transactions))) + str(self.block_data.previous_hash) + str(self.block_data.proof)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return {
            "hash": self.hash,
            "index": self.block_data.index,
            "timestamp": self.block_data.timestamp,
            "transactions": list(map(lambda x: x.repr_json(), self.block_data.transactions)),
            "previous_hash": self.block_data.previous_hash,
            "proof": self.block_data.proof
        }


def executar(campos):
    transacoes = [Transacao(descricao) for descricao in campos["transacoes"]]
    block_data = BlockData(campos["index"], campos["timestamp"], transacoes, campos["previous_hash"], campos.get("proof"))
    bloco = Block(block_data)
    return bloco.repr_json()
