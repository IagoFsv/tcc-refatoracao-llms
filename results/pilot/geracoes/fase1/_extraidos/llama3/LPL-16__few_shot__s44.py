from dataclasses import dataclass, asdict

@dataclass
class TransactionFields:
    sender: str
    receiver: str
    amount: float
    timestamp: str

def executar(transaction_fields: TransactionFields):
    transaction = Transaction(
        sender=transaction_fields.sender,
        receiver=transaction_fields.receiver,
        amount=transaction_fields.amount,
        timestamp=transaction_fields.timestamp
    )
    return transaction.repr_json()
