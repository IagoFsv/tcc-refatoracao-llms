"""Bloco de uma cadeia de blocos: dados, hash e representacao em dicionario.

Ponto de entrada publico: executar(campos). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

import hashlib
from typing import List

class Transacao:
    """Transacao minima, so com o que o bloco usa: hash e repr_json."""

    def __init__(self, descricao):
        self.descricao = descricao

    @property
    def hash(self):
        return hashlib.sha256(self.descricao.encode('utf-8')).hexdigest()

    def repr_json(self):
        return  {"descricao": self.descricao}

class Campos:
    """Classe para agrupar os campos do bloco."""

    def __init__(self, index: int, timestamp: str, transacoes: List[str], previous_hash: str, proof: str = None):
        self.index = index
        self.timestamp = timestamp
        self.transacoes = transacoes
        self.previous_hash = previous_hash
        self.proof = proof

class Block:
    def __init__(self, campos: Campos):
        self.campos = campos

    @property
    def hash(self):
        return hashlib.sha256((str(self.campos.index) + str(self.campos.timestamp) + 
                               "".join(list(map(lambda x: x.hash, self.campos.transacoes))) + 
                               str(self.campos.previous_hash) + 
                               str(self.campos.proof)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return  {
            "hash": self.hash,
            "index": self.campos.index,
            "timestamp": self.campos.timestamp,
            "transactions": list(map(lambda x: x.repr_json(), self.campos.transacoes)),
            "previous_hash": self.campos.previous_hash,
            "proof": self.campos.proof
        }

def executar(campos: Campos):
    """campos: index, timestamp, transacoes  (descricoes), previous_hash e,
    opcionalmente, proof. Devolve a representacao do bloco em dicionario."""
    transacoes = [Transacao(descricao) for descricao in campos.transacoes]
    campos.transacoes = transacoes
    bloco = Block(campos)
    return bloco.repr_json()
