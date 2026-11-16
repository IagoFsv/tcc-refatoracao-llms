from dataclasses import dataclass, asdict

@dataclass
class Parametro:
    formato: tuple

def vazio(*formato):
    if any(dimensao < 0 for dimensao in formato):
        raise RuntimeError(f"Trying to create tensor with negative dimension:  {list(formato)}")
    return Parametro(formato)

@dataclass
class Linear:
    in_features: int
    out_features: int
    bias: bool

    def parametros(self):
        return [p for p in (self.weight, self.bias) if p is not None]

@dataclass
class ReLU:
    inplace: bool

    def parametros(self):
        return []

@dataclass
class Sequential:
    camadas: list

    def parameters(self):
        return iter([p for camada in self.camadas for p in camada.parametros()])

@dataclass
class Adam:
    params: list
    lr: float

@dataclass
class MSELoss:
    reduction: str

@dataclass
class DQN:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float

    def __init__(self, input_size, n_actions, hidden_size, gamma):
        # define the neural network
        self.model = Sequential([
            Linear(input_size, hidden_size, True),
            ReLU(False),
            Linear(hidden_size, n_actions, True)
        ])
        # define the optimizer
        self.optimizer = Adam(self.model.parameters(), 0.001)
        # define the loss function
        self.loss_fn = MSELoss("mean")

def resumo(rede):
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
    return resumo(rede)
