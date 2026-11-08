from dataclasses import dataclass, asdict

@dataclass
class Transacao:
    descricao: str

@dataclass
class Block:
    index: int
    timestamp: str
    transacoes: list
    previous_hash: str
    proof: str = None

def executar(campos):
    transacoes = [Transacao(descricao) for descricao in campos["transacoes"]]
    bloco = Block(**campos, transacoes=transacoes)
    return bloco.repr_json()

Block.__dict__['hash'] = property(lambda self: hashlib.sha256((str(self.index) + str(self.timestamp) + "".join(list(map(lambda x: x.descricao, self.transacoes))) + str(self.previous_hash) + str(self.proof)).encode('utf-8')).hexdigest())

Block.__dict__['repr_json'] = property(lambda self: {
    "hash": self.hash,
    "index": self.index,
    "timestamp": self.timestamp,
    "transactions": list(map(lambda x: {"descricao": x.descricao}, self.transacoes)),
    "previous_hash": self.previous_hash,
    "proof": self.proof
})
