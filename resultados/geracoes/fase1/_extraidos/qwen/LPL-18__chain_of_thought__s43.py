import random

class DQN:
    """Rede minima: dimensoes recebidas e pesos copiaveis."""

    def __init__(self, *dimensoes):
        input_size, n_actions, hidden_size, gamma = dimensoes
        if min(input_size, n_actions, hidden_size) < 0:
            raise RuntimeError("Trying to create tensor with negative dimension")
        self.dimensoes = dimensoes
        self.pesos = {"pesos": object()}

    def state_dict(self):
        return dict(self.pesos)

    def load_state_dict(self, state_dict):
        self.pesos = dict(state_dict)


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


class Configuracao:
    def __init__(self, input_size, n_actions, hidden_size, gamma, batch_size, epsilon, epsilon_min, epsilon_decay):
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma
        self.batch_size = batch_size
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay


class DQNAgent:
    def __init__(self, configuracao):
        self.input_size = configuracao.input_size
        self.n_actions = configuracao.n_actions
        self.hidden_size = configuracao.hidden_size
        self.gamma = configuracao.gamma
        self.batch_size = configuracao.batch_size
        self.epsilon = configuracao.epsilon
        self.epsilon_min = configuracao.epsilon_min
        self.epsilon_decay = configuracao.epsilon_decay
        self.memory = ReplayMemory(capacity=1000)
        self.dqn = DQN(configuracao.input_size, configuracao.n_actions, configuracao.hidden_size, configuracao.gamma)
        self.target_dqn = DQN(configuracao.input_size, configuracao.n_actions, configuracao.hidden_size, configuracao.gamma)
        self.target_dqn.load_state_dict(self.dqn.state_dict())


def _resumo(agente):
    """Hiperparametros guardados, memoria, as duas redes e a sincronia entre elas."""
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
    """configuracao: input_size, n_actions, hidden_size, gamma, batch_size,
    epsilon, epsilon_min e epsilon_decay."""
    agente = DQNAgent(configuracao)
    return _resumo(agente)
