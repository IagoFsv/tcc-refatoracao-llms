import hashlib

class TransactionParameters:
    def __init__(self, sender, receiver, amount, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp

class Transaction:
    def __init__(self, params: TransactionParameters):
        self.params = params
        self.public_key = None
        self.signature = None

    @property
    def hash(self):
        return hashlib.sha256((str(self.params.sender) + str(self.params.receiver) + str(self.params.amount) + str(self.params.timestamp)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return {
            "sender": self.params.sender,
            "receiver": self.params.receiver,
            "amount": self.params.amount,
            "timestamp": self.params.timestamp,
            "hash": self.hash
        }

def executar(campos):
    params = TransactionParameters(campos["sender"], campos["receiver"], campos["amount"], campos["timestamp"])
    transacao = Transaction(params)
    return transacao.repr_json()
