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


class RedeConfig(SimpleNamespace):
    def __init__(self, input_size, n_actions, hidden_size, gamma):
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma


class DQN:
    def __init__(self, config):
        # define the neural network
        self.model = torch.nn.Sequential(
            torch.nn.Linear(config.input_size, config.hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(config.hidden_size, config.n_actions)
        )
        # define the optimizer
        self.optimizer = torch.optim.Adam(self.model.parameters())
        # define the loss function
        self.loss_fn = torch.nn.MSELoss()
        # define the discount factor
        self.gamma = config.gamma
        self.n_actions = config.n_actions


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


def executar(config):
    """config: RedeConfig com input_size, n_actions, hidden_size e gamma."""
    rede = DQN(config)
    return _resumo(rede)
