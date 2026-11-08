class _Transacao:
    # ...

class Block(object):
    # ...

class BlockCreationParams:
    def __init__(self, index, timestamp, transactions, previous_hash, proof=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof

def executar(params):
    transacoes = [_Transacao(descricao) for descricao in params.transactions]
    if params.proof:
        bloco = Block(params.index, params.timestamp, transacoes, params.previous_hash, params.proof)
    else:
        bloco = Block(params.index, params.timestamp, transacoes, params.previous_hash)
    return bloco.repr_json()
