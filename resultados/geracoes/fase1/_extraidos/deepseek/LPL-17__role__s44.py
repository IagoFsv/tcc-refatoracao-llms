from types import SimpleNamespace


class Parameter:
    def __init__(self, formato):
        self.formato = formato


def empty(*formato):
    if any(dimension < 0 for dimension in formato):
        raise RuntimeError(f"Trying to create tensor with negative dimension:  {list(formato)}")
    return Parameter(formato)


class Linear:
    def __init__(self, in_features, out_features, bias=True):
        self.description = ("Linear", in_features, out_features, bias)
        self.weight = empty(out_features, in_features)
        self.bias = empty(out_features) if bias else None

    def parameters(self):
        return [p for p in (self.weight, self.bias) if p is not None]


class ReLU:
    def __init__(self, inplace=False):
        self.description = ("ReLU", inplace)

    def parameters(self):
        return []


class Sequential:
    def __init__(self, *layers):
        self.layers = layers

    def parameters(self):
        return iter([p for layer in self.layers for p in layer.parameters()])


class Adam:
    def __init__(self, params, lr=0.001):
        self.params = list(params)
        if not self.params:
            raise ValueError("optimizer got an empty parameter list")
        self.lr = lr


class MSELoss:
    def __init__(self, reduction="mean"):
        self.reduction = reduction


torch = SimpleNamespace(
    nn=SimpleNamespace(Sequential=Sequential, Linear=Linear, ReLU=ReLU, MSELoss=MSELoss),
    optim=SimpleNamespace(Adam=Adam),
)


class DQN:
    def __init__(self, input_size, n_actions, hidden_size, gamma):
        self.model = torch.nn.Sequential(
            torch.nn.Linear(input_size, hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_size, n_actions)
        )
        self.optimizer = torch.optim.Adam(self.model.parameters())
        self.loss_fn = torch.nn.MSELoss()
        self.gamma = gamma
        self.n_actions = n_actions


def summary(network):
    parameters = list(network.model.parameters())
    optimizer = network.optimizer
    same = len(optimizer.params) == len(parameters) and all(
        a is b for a, b in zip(optimizer.params, parameters))
    return {
        "layers": [layer.description for layer in network.model.layers],
        "optimizer": ("Adam", [p.formato for p in optimizer.params], optimizer.lr, same),
        "loss": ("MSELoss", network.loss_fn.reduction),
        "gamma": network.gamma,
        "n_actions": network.n_actions,
    }


def execute(dimensions):
    network = DQN(dimensions["input_size"], dimensions["n_actions"],
                  dimensions["hidden_size"], dimensions["gamma"])
    return summary(network)
