from dataclasses import dataclass, asdict

@dataclass
class TransactionData:
    sender: str
    receiver: str
    amount: int
    timestamp: str

def executar(campos: TransactionData):
    transacao = Transaction(campos.sender, campos.receiver, campos.amount, campos.timestamp)
    return transacao.repr_json()
