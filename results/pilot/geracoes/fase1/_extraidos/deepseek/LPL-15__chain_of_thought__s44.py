import hashlib

class Transacao:
    def __init__(self, descricao):
        self.descricao = descricao

    @property
    def hash(self):
        return hashlib.sha256(self.descricao.encode('utf-8')).hexdigest()

    def repr_json(self):
        return  {"descricao": self.descricao}


class BlockParams:
    def __init__(self, index, timestamp, transactions, previous_hash, proof=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof


class Block:
    def __init__(self, params: BlockParams):
        self.params = params

    @property
    def hash(self):
        return hashlib.sha256((str(self.params.index) 
                               + str(self.params.timestamp) 
                               + "".join(list(map(lambda x: x.hash, self.params.transactions))) 
                               + str(self.params.previous_hash) 
                               + str(self.params.proof)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return  {
            "hash": self.hash,
            "index": self.params.index,
            "timestamp": self.params.timestamp,
            "transactions": list(map(lambda x: x.repr_json(), self.params.transactions)),
            "previous_hash": self.params.previous_hash,
            "proof": self.params.proof
        }


def executar(campos):
    transacoes = [Transacao(descricao) for descricao in campos["transacoes"]]
    params = BlockParams(campos["index"], campos["timestamp"], transacoes, campos["previous_hash"], campos.get("proof"))
    bloco = Block(params)
    return bloco.repr_json()
