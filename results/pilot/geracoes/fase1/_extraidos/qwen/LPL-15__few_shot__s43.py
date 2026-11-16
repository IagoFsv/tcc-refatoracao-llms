import hashlib
from dataclasses import dataclass, asdict

@dataclass
class Transacao:
    descricao: str

    @property
    def hash(self):
        return hashlib.sha256(self.descricao.encode('utf-8')).hexdigest()

    def repr_json(self):
        return {"descricao": self.descricao}

@dataclass
class CamposBloco:
    index: int
    timestamp: str
    transacoes: list
    previous_hash: str
    proof: str = None

class Block(object):
    def __init__(self, campos: CamposBloco):
        self.index = campos.index
        self.timestamp = campos.timestamp
        self.transactions = [_Transacao(descricao) for descricao in campos.transacoes]
        self.previous_hash = campos.previous_hash
        self.proof = campos.proof

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

def executar(campos):
    bloco = Block(CamposBloco(**campos))
    return bloco.repr_json()
