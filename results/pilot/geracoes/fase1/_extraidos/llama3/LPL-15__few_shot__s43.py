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
class Block:
    index: int
    timestamp: str
    transactions: list[Transacao]
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


def executar(block_data):
    """block_data: BlockData. Devolve a representacao do bloco em dicionario."""
    block = Block(**block_data)
    return block.repr_json()

class BlockData:
    def __init__(self, index, timestamp, transactions, previous_hash, proof=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = [Transacao(descricao) for descricao in transactions]
        self.previous_hash = previous_hash
        self.proof = proof

    def __dict__(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [t.repr_json() for t in self.transactions],
            "previous_hash": self.previous_hash,
            "proof": self.proof
        }
