class TransactionParams(object):
    def __init__(self, sender, receiver, amount, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp

def executar(params):
    """params: uma instância da classe TransactionParams. Devolve a representação
    da transação em dicionário."""
    transacao = Transaction(params.sender, params.receiver, params.amount, params.timestamp)
    return transacao.repr_json()
