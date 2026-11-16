from dataclasses import dataclass, asdict

@dataclass
class Transaction:
    descricao: str

    @property
    def hash(self):
        return hashlib.sha256(self.descricao.encode('utf-8')).hexdigest()

    def repr_json(self):
        return {"descricao": self.descricao}

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

def executar(transactions):
    """Devolve a representacao do bloco em dicionario."""
    bloco = Block(0, "0", [Transaction(descricao) for descricao in transactions], "0")
    return bloco.repr_json()
