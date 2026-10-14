"""Bloco de uma cadeia de blocos: dados, hash e representacao em dicionario.

Ponto de entrada publico: executar(campos). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

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
    def __init__(self, index, timestamp, transactions, previous_hash, proof=None, *args, **kwargs):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof

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
    """campos: index, timestamp, transacoes (descricoes), previous_hash e,
    opcionalmente, proof. Devolve a representacao do bloco em dicionario."""
    transacoes = [_Transacao(descricao) for descricao in campos["transacoes"]]
    if "proof" in campos:
        bloco = Block(campos["index"], campos["timestamp"], transacoes,
                      campos["previous_hash"], campos["proof"])
    else:
        bloco = Block(campos["index"], campos["timestamp"], transacoes,
                      campos["previous_hash"])
    return bloco.repr_json()
