from dataclasses import dataclass, asdict

@dataclass
class Produto:
    nome: str
    preco: float
    quantidade: int
    categoria: str
    fornecedor: str
    desconto: float

def cadastrar_produto(produto: Produto):
    banco_de_dados.salvar(asdict(produto))
    return produto
