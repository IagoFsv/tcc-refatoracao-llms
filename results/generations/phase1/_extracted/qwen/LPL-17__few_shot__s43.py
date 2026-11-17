from dataclasses import dataclass, asdict

@dataclass
class NetworkConfig:
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

class DQN:
    def __init__(self, config: NetworkConfig, optimizer_config: OptimizerConfig, loss_config: LossConfig):
        # define the neural network
        self.model = torch.nn.Sequential(
            torch.nn.Linear(config.input_size, config.hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(config.hidden_size, config.n_actions)
        )
        # define the optimizer
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=optimizer_config.lr)
        # define the loss function
        self.loss_fn = torch.nn.MSELoss(reduction=loss_config.reduction)
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


def run(dimensions):
    """dimensions: input_size, n_actions, hidden_size and gamma. Public entry point of this unit."""
    network_config = NetworkConfig(**dimensions)
    optimizer_config = OptimizerConfig(lr=dimensions["lr"])
    loss_config = LossConfig(reduction=dimensions["loss_reduction"])
    network = DQN(network_config, optimizer_config, loss_config)
    return _summary(network)
