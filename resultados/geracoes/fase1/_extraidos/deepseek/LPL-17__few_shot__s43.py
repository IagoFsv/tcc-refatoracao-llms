from types import SimpleNamespace


class Parameter:
    def __init__(self, formato):
        self.formato = formato


def empty(*formato):
    if any(dimensao < 0 for dimensao in formato):
        raise RuntimeError(f"Trying to create tensor with negative dimension:  {list(formato)}")
    return Parameter(formato)


class Linear:
    def __init__(self, in_features, out_features, bias=True):
        self.descricao = ("Linear", in_features, out_features, bias)
        self.weight = empty(out_features, in_features)
        self.bias = empty(out_features) if bias else None

    def parameters(self):
        return [p for p in (self.weight, self.bias) if p is not None]


class ReLU:
    def __init__(self, inplace=False):
        self.descricao = ("ReLU", inplace)

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


def summary(net):
    """Layers in order, optimizer, loss and the two stored values."""
    params = list(net.model.parameters())
    optimizer = net.optimizer
    same = len(optimizer.params) == len(params) and all(
        a is b for a, b in zip(optimizer.params, params))
    return {
        "layers": [layer.descricao for layer in net.model.layers],
        "optimizer": ("Adam", [p.formato for p in optimizer.params], optimizer.lr, same),
        "loss": ("MSELoss", net.loss_fn.reduction),
        "gamma": net.gamma,
        "n_actions": net.n_actions,
    }


def run(dimensions):
    """dimensions: input_size, n_actions, hidden_size and gamma."""
    net = DQN(dimensions["input_size"], dimensions["n_actions"],
              dimensions["hidden_size"], dimensions["gamma"])
    return summary(net)
