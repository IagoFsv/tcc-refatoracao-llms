import hashlib

class Transaction(object):
    def __init__(self, transaction_data):
        self.sender = transaction_data.sender
        self.receiver = transaction_data.receiver
        self.amount = transaction_data.amount
        self.timestamp = transaction_data.timestamp
        self.public_key = None
        self.signature = None

    @property
    def hash(self):
        return hashlib.sha256((str(self.sender) + str(self.receiver) + str(self.amount) + str(self.timestamp)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "hash": self.hash
        }

class TransactionData(object):
    def __init__(self, sender, receiver, amount, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp

def executar(transaction_data):
    """Devolve a representacao da transacao em dicionario."""
    transacao = Transaction(transaction_data)
    return transacao.repr_json()

