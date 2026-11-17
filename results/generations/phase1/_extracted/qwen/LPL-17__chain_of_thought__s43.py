"""Deep Q-network: layers, optimizer and loss function.

Public entry point: run(dimensions). Do not change its name or signature; the
rest of the file may be freely reorganized.

The network pieces (linear layer, ReLU, sequence, Adam optimizer, squared
loss) are minimal versions that only keep the configuration they receive.
The linear layer creates the weights with shape (outputs, inputs) and the
bias with (outputs,), and refuses a negative size, like the real version.
"""

from types import SimpleNamespace


class _Parameter:
    def __init__(self, shape):
        self.shape = shape


def _empty(*shape):
    if any(dimension < 0 for dimension in shape):
        raise RuntimeError(f"Trying to create tensor with negative dimension: {list(shape)}")
    return _Parameter(shape)


class _Linear:
    def __init__(self, in_features, out_features, bias=True):
        self.description = ("Linear", in_features, out_features, bias)
        self.weight = _empty(out_features, in_features)
        self.bias = _empty(out_features) if bias else None

    def own_parameters(self):
        return [p for p in (self.weight, self.bias) if p is not None]


class _ReLU:
    def __init__(self, inplace=False):
        self.description = ("ReLU", inplace)

    def own_parameters(self):
        return []


class _Sequential:
    def __init__(self, *layers):
        self.layers = layers

    def parameters(self):
        return iter([p for layer in self.layers for p in layer.own_parameters()])


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


class NetworkParameters:
    def __init__(self, input_size, n_actions, hidden_size, gamma):
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma


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


def _summary(network):
    """Layers in order, optimizer, loss and the two stored values."""
    parameters = list(network.model.parameters())
    optimizer = network.optimizer
    same = len(optimizer.params) == len(parameters) and all(
        a is b for a, b in zip(optimizer.params, parameters))
    return {
        "layers": [layer.description for layer in network.model.layers],
        "optimizer": ("Adam", [p.shape for p in optimizer.params], optimizer.lr, same),
        "loss": ("MSELoss", network.loss_fn.reduction),
        "gamma": network.gamma,
        "n_actions": network.n_actions,
    }


def run(parameters: NetworkParameters):
    """parameters: NetworkParameters object. Public entry point of this unit."""
    network = DQN(parameters.input_size, parameters.n_actions,
                  parameters.hidden_size, parameters.gamma)
    return _summary(network)
