class BlockFields:
    def __init__(self, index, timestamp, transactions, previous_hash, proof=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof


def executar(block_fields):
    """block_fields: objeto com os campos necessários para criar um bloco.
    Devolve a representacao do bloco em dicionario."""
    transacoes = [_Transacao(descricao) for descricao in block_fields.transactions]
    if block_fields.proof:
        bloco = Block(block_fields.index, block_fields.timestamp, transacoes, block_fields.previous_hash, block_fields.proof)
    else:
        bloco = Block(block_fields.index, block_fields.timestamp, transacoes, block_fields.previous_hash)
    return bloco.repr_json()
