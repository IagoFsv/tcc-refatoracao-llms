"""Transacao entre duas partes: dados, hash e representacao em dicionario.

Ponto de entrada publico: executar(campos). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

import hashlib


class TransactionData(object):
    def __init__(self, sender, receiver, amount, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp


class Transaction(object):
    def __init__(self, transaction_data):
        self.transaction_data = transaction_data
        self.public_key = None
        self.signature = None

    @property
    def hash(self):
        return hashlib.sha256((str(self.transaction_data.sender) + str(self.transaction_data.receiver) + str(self.transaction_data.amount) + str(self.transaction_data.timestamp)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return self.transaction_data.repr_json()


def executar(campos):
    """campos: sender, receiver, amount e timestamp. Devolve a representacao
    da transacao em dicionario."""
    transacao_data = TransactionData(campos["sender"], campos["receiver"], campos["amount"], campos["timestamp"])
    transacao = Transaction(transacao_data)
    return transacao.repr_json()
