from dataclasses import dataclass, field
from typing import List

@dataclass
class Endereco:
    cidade: str
    cep: str

@dataclass
class Cliente:
    nome: str
    endereco: Endereco

@dataclass
class Item:
    produto: str
    qtd: int

@dataclass
class Pedido:
    cliente: Cliente
    itens: List[Item] = field(default_factory=list)

dados = [
    Pedido(
        cliente=Cliente(
            nome='Ana',
            endereco=Endereco(cidade='Fortaleza', cep='60000-000')
        ),
        itens=[Item('caneta', 2), Item('caderno', 1)]
    )
]
