from dataclasses import dataclass, asdict
import hashlib

@dataclass
class TransactionParams:
    sender: str
    receiver: str
    amount: float
    timestamp: str

class Transaction(object):
    def __init__(self, params: TransactionParams, *args, **kwargs):
        self.params = params
        self.public_key = None
        self.signature = None

    @property
    def hash(self):
        return hashlib.sha256((str(self.params.sender) + str(self.params.receiver) + str(self.params.amount) + str(self.params.timestamp)).encode('utf-8')).hexdigest()

    def repr_json(self):
        return asdict(self.params) | {
            "hash": self.hash
        }

def executar(campos):
    params = TransactionParams(campos["sender"], campos["receiver"], campos["amount"], campos["timestamp"])
    transacao = Transaction(params)
    return transacao.repr_json()
