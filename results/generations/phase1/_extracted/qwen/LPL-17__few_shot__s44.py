from dataclasses import dataclass, asdict

@dataclass
class DQNConfig:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float

@dataclass
class OptimizerConfig:
    lr: float

@dataclass
class LossConfig:
    reduction: str

@dataclass
class NetworkConfig:
    dqn: DQNConfig
    optimizer: OptimizerConfig
    loss: LossConfig

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


def run(config: NetworkConfig):
    """config: DQNConfig, OptimizerConfig, LossConfig. Public entry point of this unit."""
    network = DQN(
        config.dqn.input_size,
        config.dqn.n_actions,
        config.dqn.hidden_size,
        config.dqn.gamma
    )
    return _summary(network)
