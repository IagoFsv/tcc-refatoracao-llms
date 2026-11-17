from dataclasses import dataclass, asdict

@dataclass
class Configuration:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float
    batch_size: int
    epsilon: float
    epsilon_min: float
    epsilon_decay: float

class DQN:
    """Minimal network: received dimensions and copyable weights."""

    def __init__(self, *dimensions):
        input_size, n_actions, hidden_size, gamma = dimensions
        if min(input_size, n_actions, hidden_size) < 0:
            raise RuntimeError("Trying to create tensor with negative dimension")
        self.dimensions = dimensions
        self.weights = {"weights": object()}

    def state_dict(self):
        return dict(self.weights)

    def load_state_dict(self, state_dict):
        self.weights = dict(state_dict)


class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, *args):
        self.memory.append(args)
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        return zip(*random.sample(self.memory, batch_size))
    
    def len(self):
        return len(self.memory)


class DQNAgent:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.memory = ReplayMemory(capacity=1000)
        self.dqn = DQN(configuration.input_size, configuration.n_actions, configuration.hidden_size, configuration.gamma)
        self.target_dqn = DQN(configuration.input_size, configuration.n_actions, configuration.hidden_size, configuration.gamma)
        self.target_dqn.load_state_dict(self.dqn.state_dict())


def _summary(agent):
    """Stored hyperparameters, memory, both networks and whether they are in sync."""
    names = ("input_size", "n_actions", "hidden_size", "gamma", "batch_size", "epsilon", "epsilon_min", "epsilon_decay")
    return {
        "hyperparameters": {name: getattr(agent.configuration, name) for name in names},
        "memory": (agent.memory.capacity, agent.memory.len()),
        "networks": (agent.dqn.dimensions, agent.target_dqn.dimensions),
        "distinct_networks": agent.dqn is not agent.target_dqn,
        "target_in_sync": agent.target_dqn.state_dict()["weights"] is agent.dqn.state_dict()["weights"],
    }


def run(configuration: Configuration):
    """Public entry point of this unit."""
    agent = DQNAgent(configuration)
    return _summary(agent)
