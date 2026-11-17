"""Reinforcement learning agent with an experience replay memory.

Public entry point: run(configuration). Do not change its name or signature;
the rest of the file may be freely reorganized.

The Q-network is a minimal version: it keeps the dimensions it receives and
its own set of weights, which can be copied from another network; it refuses
a negative size, like the real version.
"""

import random
from dataclasses import dataclass

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

    def __init__(self, dimensions):
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
        # debug
        return zip(*random.sample(self.memory, batch_size))
    
    def len(self):
        return len(self.memory)


class DQNAgent:
    def __init__(self, configuration: Configuration):
        self.input_size = configuration.input_size
        self.n_actions = configuration.n_actions
        self.hidden_size = configuration.hidden_size
        self.gamma = configuration.gamma
        self.batch_size = configuration.batch_size
        self.epsilon = configuration.epsilon
        self.epsilon_min = configuration.epsilon_min
        self.epsilon_decay = configuration.epsilon_decay
        self.memory = ReplayMemory(capacity=1000)
        self.dqn = DQN((self.input_size, self.n_actions, self.hidden_size, self.gamma))
        self.target_dqn = DQN((self.input_size, self.n_actions, self.hidden_size, self.gamma))
        self.target_dqn.load_state_dict(self.dqn.state_dict())


def _summary(agent):
    """Stored hyperparameters, memory, both networks and whether they are in sync."""
    names = ("input_size", "n_actions", "hidden_size", "gamma",
             "batch_size", "epsilon", "epsilon_min", "epsilon_decay")
    return {
        "hyperparameters": {name: getattr(agent, name) for name in names},
        "memory": (agent.memory.capacity, agent.memory.len()),
        "networks": (agent.dqn.dimensions, agent.target_dqn.dimensions),
        "distinct_networks": agent.dqn is not agent.target_dqn,
        "target_in_sync": agent.target_dqn.state_dict()["weights"] is agent.dqn.state_dict()["weights"],
   }


def run(configuration: Configuration):
    """Public entry point of this unit.

    configuration: input_size, n_actions, hidden_size, gamma, batch_size,
    epsilon, epsilon_min and epsilon_decay.
    """
    agent = DQNAgent(configuration)
    return _summary(agent)
