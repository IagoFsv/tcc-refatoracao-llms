"""Transacao entre duas partes: dados, hash e representacao em dicionario.

Ponto de entrada publico: executar(campos). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

import hashlib


class Transaction(object):
    def __init__(self, sender, receiver, amount, timestamp,  *args, **kwargs):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp
        self.public_key = None
        self.signature = None

    
    @property
    def hash(self):
        return hashlib.sha256((str(self.sender) + str(self.receiver) + str(self.amount) + str(self.timestamp)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return  {
             "sender": self.sender,
             "receiver": self.receiver,
             "amount": self.amount,
             "timestamp": self.timestamp,
             "hash": self.hash
         }


class TransactionData:
    def __init__(self, campos):
        self.sender = campos["sender"]
        self.receiver = campos["receiver"]
        self.amount = campos["amount"]
        self.timestamp = campos["timestamp"]


def executar(campos):
    """campos: sender, receiver, amount e timestamp. Devolve a representacao
    da transacao em dicionario."""
    transacao_data = TransactionData(campos)
    transacao = Transaction(transacao_data.sender, transacao_data.receiver, transacao_data.amount,
                            transacao_data.timestamp)
    return transacao.repr_json()
