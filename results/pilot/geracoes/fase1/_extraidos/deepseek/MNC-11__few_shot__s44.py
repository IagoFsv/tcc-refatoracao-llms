import toml
from invoke import Context, task
from invoke.exceptions import UnexpectedExit
from invoke.runners import Result

class Endereco:
    def __init__(self, cidade: str, cep: str):
        self.cidade = cidade
        self.cep = cep

class Cliente:
    def __init__(self, nome: str, endereco: Endereco):
        self.nome = nome
        self.endereco = endereco

class Item:
    def __init__(self, produto: str, qtd: int):
        self.produto = produto
        self.qtd = qtd

class Pedido:
    def __init__(self, cliente: Cliente, itens: List[Item]):
        self.cliente = cliente
        self.itens = itens

dados = [
    Pedido(
        cliente=Cliente(
            nome='Ana',
            endereco=Endereco(cidade='Fortaleza', cep='60000-000')
        ),
        itens=[Item('caneta', 2), Item('caderno', 1)]
    )
]
