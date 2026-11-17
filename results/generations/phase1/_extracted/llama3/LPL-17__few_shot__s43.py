from types import SimpleNamespace
from dataclasses import dataclass, asdict


@dataclass
class NetworkConfig:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float


@dataclass
class Layer:
    description: str
    shape: tuple


@dataclass
class Linear(Layer):
    in_features: int
    out_features: int
    bias: bool = True

    def own_parameters(self):
        return [self] if self.bias else []


@dataclass
class ReLU(Layer):
    inplace: bool = False

    def own_parameters(self):
        return []


@dataclass
class Sequential:
    layers: list

    def parameters(self):
        return iter([p for layer in self.layers for p in layer.own_parameters()])


@dataclass
class Adam:
    params: list
    lr: float = 0.001


@dataclass
class MSELoss:
    reduction: str = "mean"


torch = SimpleNamespace(
    nn=SimpleNamespace(Sequential=Sequential, Linear=Linear, ReLU=ReLU, MSELoss=MSELoss),
    optim=SimpleNamespace(Adam=Adam),
)


class DQN:
    def __init__(self, config: NetworkConfig):
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


def run(config):
    """Public entry point of this unit."""
    network = DQN(config)
    return _summary(network)
