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


class Block(object):
    def __init__(self, campos):
        self.index = campos["index"]
        self.timestamp = campos["timestamp"]
        self.transactions = [_Transacao(descricao) for descricao in campos["transacoes"]]
        self.previous_hash = campos["previous_hash"]
        if "proof" in campos:
            self.proof = campos["proof"]
        else:
            self.proof = None

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
    """campos: um dicionario com index, timestamp, transacoes (descricoes), previous_hash e,
    opcionalmente, proof. Devolve a representacao do bloco em dicionario."""
    return Block(campos).repr_json()
