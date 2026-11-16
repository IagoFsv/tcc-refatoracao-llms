import random

class DQNConfig:
    def __init__(self, input_size, n_actions, hidden_size, gamma):
        if min(input_size, n_actions, hidden_size) < 0:
            raise RuntimeError("Trying to create tensor with negative dimension")
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma

class ReplayMemoryConfig:
    def __init__(self, capacity):
        self.capacity = capacity

class DQNAgentConfig:
    def __init__(self, dqn_config, replay_memory_config, batch_size, epsilon, epsilon_min, epsilon_decay):
        self.dqn_config = dqn_config
        self.replay_memory_config = replay_memory_config
        self.batch_size = batch_size
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

class DQN:
    """Rede minima: dimensoes recebidas e pesos copiaveis."""

    def __init__(self, config):
        self.dimensoes = (config.input_size, config.n_actions, config.hidden_size, config.gamma)
        self.pesos = {"pesos": object()}

    def state_dict(self):
        return dict(self.pesos)

    def load_state_dict(self, state_dict):
        self.pesos = dict(state_dict)


class ReplayMemory:
    def __init__(self, config):
        self.capacity = config.capacity
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
    def __init__(self, config):
        self.input_size = config.dqn_config.input_size
        self.n_actions = config.dqn_config.n_actions
        self.hidden_size = config.dqn_config.hidden_size
        self.gamma = config.dqn_config.gamma
        self.batch_size = config.batch_size
        self.epsilon = config.epsilon
        self.epsilon_min = config.epsilon_min
        self.epsilon_decay = config.epsilon_decay
        self.memory = ReplayMemory(config.replay_memory_config)
        self.dqn = DQN(config.dqn_config)
        self.target_dqn = DQN(config.dqn_config)
        self.target_dqn.load_state_dict(self.dqn.state_dict())


def _resumo(agente):
    nomes = ("input_size", "n_actions", "hidden_size", "gamma",
             "batch_size", "epsilon", "epsilon_min", "epsilon_decay")
    return {
        "hiperparametros": {nome: getattr(agente, nome) for nome in nomes},
        "memoria": (agente.memory.capacity, agente.memory.len()),
        "redes": (agente.dqn.dimensoes, agente.target_dqn.dimensoes),
        "redes_distintas": agente.dqn is not agente.target_dqn,
        "alvo_sincronizado": agente.target_dqn.state_dict()["pesos"] is agente.dqn.state_dict()["pesos"],
    }


def executar(configuracao):
    dqn_config = DQNConfig(**configuracao)
    replay_memory_config = ReplayMemoryConfig(capacity=1000)
    agent_config = DQNAgentConfig(dqn_config, replay_memory_config, **configuracao)
    agente = DQNAgent(agent_config)
    return _resumo(agente)
