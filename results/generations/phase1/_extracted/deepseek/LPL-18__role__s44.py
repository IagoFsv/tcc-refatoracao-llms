"""Reinforcement learning agent with an experience replay memory.

Public entry point: run(configuration). Do not change its name or signature;
the rest of the file may be freely reorganized.

The Q-network is a minimal version: it keeps the dimensions it receives and
its own set of weights, which can be copied from another network; it refuses
a negative size, like the real version.
"""

import random


class Params:
    """Class to hold the parameters of the DQN."""

    def __init__(self, input_size, n_actions, hidden_size, gamma):
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma


class DQN:
    """Minimal network: received dimensions and copyable weights."""

    def __init__(self, params: Params):
        if min(params.input_size, params.n_actions, params.hidden_size) < 0:
            raise RuntimeError("Trying to create tensor with negative dimension")
        self.params = params
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
    def __init__(self, params: Params, batch_size, epsilon, epsilon_min, epsilon_decay):
        # define the hyperparameters
        self.params = params
        self.batch_size = batch_size
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        # create the replay memory
        self.memory = ReplayMemory(capacity=1000)
        # create the DQN
        self.dqn = DQN(params)
        # create the target DQN
        self.target_dqn = DQN(params)
        # initialize the target DQN
        self.target_dqn.load_state_dict(self.dqn.state_dict())


def _summary(agent):
    """Stored hyperparameters, memory, both networks and whether they are in sync."""
    names = ("input_size", "n_actions", "hidden_size", "gamma",
             "batch_size", "epsilon", "epsilon_min", "epsilon_decay")
    return {
        "hyperparameters": {name: getattr(agent.params, name) for name in names},
        "memory": (agent.memory.capacity, agent.memory.len()),
        "networks": (agent.dqn.params, agent.target_dqn.params),
        "distinct_networks": agent.dqn is not agent.target_dqn,
        "target_in_sync": agent.target_dqn.state_dict()["weights"] is agent.dqn.state_dict()["weights"],
    }


def run(configuration):
    """Public entry point of this unit.

    configuration: input_size, n_actions, hidden_size, gamma, batch_size,
    epsilon, epsilon_min and epsilon_decay.
    """
    c = configuration
    params = Params(c["input_size"], c["n_actions"], c["hidden_size"], c["gamma"])
    agent = DQNAgent(params, c["batch_size"], c["epsilon"], c["epsilon_min"], c["epsilon_decay"])
    return _summary(agent)
