import hashlib

class TransactionFields(object):
    def __init__(self, sender, receiver, amount, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp

class Transaction(object):
    def __init__(self, fields: TransactionFields):
        self.fields = fields
        self.public_key = None
        self.signature = None

    @property
    def hash(self):
        return hashlib.sha256((str(self.fields.sender) + str(self.fields.receiver) + str(self.fields.amount) + str(self.fields.timestamp)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return {
            "sender": self.fields.sender,
            "receiver": self.fields.receiver,
            "amount": self.fields.amount,
            "timestamp": self.fields.timestamp,
            "hash": self.hash
        }

def executar(campos: TransactionFields):
    """campos: sender, receiver, amount e timestamp. Devolve a representacao
    da transacao em dicionario."""
    transacao = Transaction(campos)
    return transacao.repr_json()
