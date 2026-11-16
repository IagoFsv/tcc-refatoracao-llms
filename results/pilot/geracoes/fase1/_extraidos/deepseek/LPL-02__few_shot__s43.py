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

def executar(lotes):
    """Treina por uma epoca. Ponto de entrada publico desta unidade.

    lotes: lista de 2-tuplas (amostras, rotulos); cada amostra tem um score por classe.
    Devolve uma 4-tupla (perda, acuracia, vies final do modelo, modelo em modo de treino).
    """
    modelo = _Modelo()
    loader = DataLoader([(_Tensor(a), _Tensor(r)) for a, r in lotes])
    perda, acuracia, modelo = train(modelo, "cpu", loader, _Otimizador(modelo), _Perda)
    return perda, acuracia, modelo.vies, modelo.training
