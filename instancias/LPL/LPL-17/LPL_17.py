"""Rede Q profunda: camadas, otimizador e funcao de perda.

Ponto de entrada publico: executar(dimensoes). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.

As pecas de rede (camada linear, ReLU, sequencia, otimizador Adam, perda
quadratica) sao versoes minimas que so guardam a configuracao recebida. A
camada linear cria os pesos com o formato (saidas, entradas) e o vies com
(saidas,), e recusa tamanho negativo, como a versao real.
"""

from types import SimpleNamespace


class _Parametro:
    def __init__(self, formato):
        self.formato = formato


def _vazio(*formato):
    if any(dimensao < 0 for dimensao in formato):
        raise RuntimeError(f"Trying to create tensor with negative dimension: {list(formato)}")
    return _Parametro(formato)


class _Linear:
    def __init__(self, in_features, out_features, bias=True):
        self.descricao = ("Linear", in_features, out_features, bias)
        self.weight = _vazio(out_features, in_features)
        self.bias = _vazio(out_features) if bias else None

    def parametros(self):
        return [p for p in (self.weight, self.bias) if p is not None]


class _ReLU:
    def __init__(self, inplace=False):
        self.descricao = ("ReLU", inplace)

    def parametros(self):
        return []


class _Sequential:
    def __init__(self, *camadas):
        self.camadas = camadas

    def parameters(self):
        return iter([p for camada in self.camadas for p in camada.parametros()])


class _Adam:
    def __init__(self, params, lr=0.001):
        self.params = list(params)
        if not self.params:
            raise ValueError("optimizer got an empty parameter list")
        self.lr = lr


class _MSELoss:
    def __init__(self, reduction="mean"):
        self.reduction = reduction


torch = SimpleNamespace(
    nn=SimpleNamespace(Sequential=_Sequential, Linear=_Linear, ReLU=_ReLU, MSELoss=_MSELoss),
    optim=SimpleNamespace(Adam=_Adam),
)


class DQN:
    def __init__(self, input_size, n_actions, hidden_size, gamma):
        # define the neural network
        self.model = torch.nn.Sequential(
            torch.nn.Linear(input_size, hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_size, n_actions)
        )
        # define the optimizer
        self.optimizer = torch.optim.Adam(self.model.parameters())
        # define the loss function
        self.loss_fn = torch.nn.MSELoss()
        # define the discount factor
        self.gamma = gamma
        self.n_actions = n_actions


def _resumo(rede):
    """Camadas em ordem, otimizador, perda e os dois valores guardados."""
    parametros = list(rede.model.parameters())
    otimizador = rede.optimizer
    mesmos = len(otimizador.params) == len(parametros) and all(
        a is b for a, b in zip(otimizador.params, parametros))
    return {
        "camadas": [camada.descricao for camada in rede.model.camadas],
        "otimizador": ("Adam", [p.formato for p in otimizador.params], otimizador.lr, mesmos),
        "perda": ("MSELoss", rede.loss_fn.reduction),
        "gamma": rede.gamma,
        "n_actions": rede.n_actions,
    }


def executar(dimensoes):
    """dimensoes: input_size, n_actions, hidden_size e gamma."""
    rede = DQN(dimensoes["input_size"], dimensoes["n_actions"],
               dimensoes["hidden_size"], dimensoes["gamma"])
    return _resumo(rede)
