import random


class DQN:
    """Rede minima: dimensoes recebidas e pesos copiaveis."""

    def __init__(self, configuracao):
        self.configuracao = configuracao
        self.dimensoes = self.configuracao["dimensoes"]
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


class DQNAgent:
    def __init__(self, configuracao):
        self.configuracao = configuracao
        self.input_size = self.configuracao["input_size"]
        self.n_actions = self.configuracao["n_actions"]
        self.hidden_size = self.configuracao["hidden_size"]
        self.gamma = self.configuracao["gamma"]
        self.batch_size = self.configuracao["batch_size"]
        self.epsilon = self.configuracao["epsilon"]
        self.epsilon_min = self.configuracao["epsilon_min"]
        self.epsilon_decay = self.configuracao["epsilon_decay"]
        # create the replay memory
        self.memory = ReplayMemory(capacity=1000)
        # create the DQN
        self.dqn = DQN(self.configuracao)
        # create the target DQN
        self.target_dqn = DQN(self.configuracao)
        # initialize the target DQN
        self.target_dqn.load_state_dict(self.dqn.state_dict())

    def __getattr__(self, nome):
        return getattr(self.configuracao, nome)


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
