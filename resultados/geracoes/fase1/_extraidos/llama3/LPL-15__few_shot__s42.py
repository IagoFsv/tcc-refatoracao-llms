from dataclasses import dataclass, asdict

@dataclass
class Transacao:
    descricao: str

@dataclass
class Block:
    index: int
    timestamp: str
    transactions: list[Transacao]
    previous_hash: str
    proof: str = None

def executar(bloco: Block):
    return bloco.repr_json()

def criar_bloco(index, timestamp, transacoes, previous_hash, proof=None):
    return Block(index, timestamp, [Transacao(descricao) for descricao in transacoes], previous_hash, proof)

def executar_criar_bloco(index, timestamp, transacoes, previous_hash, proof=None):
    bloco = criar_bloco(index, timestamp, transacoes, previous_hash, proof)
    return executar(bloco)
