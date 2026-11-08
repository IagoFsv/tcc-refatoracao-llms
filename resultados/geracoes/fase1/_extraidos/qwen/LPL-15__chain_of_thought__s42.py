import hashlib


class _Transacao:
    """Transacao minima, so com o que o bloco usa: hash e repr_json."""

    def __init__(self, descricao):
        self.descricao = descricao

    @property
    def hash(self):
        return hashlib.sha256(self.descricao.encode('utf-8')).hexdigest()

    def repr_json(self):
        return {"descricao": self.descricao}


class BlockFields:
    """Classe para agrupar os campos necessários para criar um bloco."""
    def __init__(self, index, timestamp, transacoes, previous_hash, proof=None):
        self.index = index
        self.timestamp = timestamp
        self.transacoes = transacoes
        self.previous_hash = previous_hash
        self.proof = proof


class Block(object):
    def __init__(self, fields):
        self.index = fields.index
        self.timestamp = fields.timestamp
        self.transactions = [_Transacao(descricao) for descricao in fields.transacoes]
        self.previous_hash = fields.previous_hash
        self.proof = fields.proof if fields.proof is not None else None

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


def executar(fields):
    """campos: index, timestamp, transacoes (descricoes), previous_hash e,
    opcionalmente, proof. Devolve a representacao do bloco em dicionario."""
    bloco = Block(fields)
    return bloco.repr_json()
