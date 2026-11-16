import hashlib
from dataclasses import dataclass, asdict

@dataclass
class TransactionData:
    sender: str
    receiver: str
    amount: float
    timestamp: str

class Transaction:
    def __init__(self, data: TransactionData):
        self.sender = data.sender
        self.receiver = data.receiver
        self.amount = data.amount
        self.timestamp = data.timestamp
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


def executar(campos):
    """campos: sender, receiver, amount e timestamp. Devolve a representacao
    da transacao em dicionario."""
    data = TransactionData(**campos)
    transacao = Transaction(data)
    return transacao.repr_json()
