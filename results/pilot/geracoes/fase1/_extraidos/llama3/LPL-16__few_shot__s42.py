from dataclasses import dataclass, asdict
import hashlib

class Transaction:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

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

@dataclass
class TransactionFields:
    sender: str
    receiver: str
    amount: float
    timestamp: str

def executar(transaction_fields: TransactionFields):
    """Devolve a representacao da transacao em dicionario."""
    transacao = Transaction(**asdict(transaction_fields))
    return transacao.repr_json()
