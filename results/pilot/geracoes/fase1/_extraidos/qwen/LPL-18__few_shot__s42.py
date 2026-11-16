from dataclasses import dataclass, asdict

@dataclass
class ConfiguracaoDQN:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float
    batch_size: int
    epsilon: float
    epsilon_min: float
    epsilon_decay: float

@dataclass
class Dimensoes:
    input_size: int
    n_actions: int
    hidden_size: int

@dataclass
class Pesos:
    pesos: object

class DQN:
    """Rede minima: dimensoes recebidas e pesos copiaveis."""

    def __init__(self, dimensoes: Dimensoes, pesos: Pesos):
        self.dimensoes = dimensoes
        self.pesos = pesos

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
        return zip(*random.sample(self.memory, batch_size))
    
    def len(self):
        return len(self.memory)


class DQNAgent:
    def __init__(self, configuracao: ConfiguracaoDQN):
        # define the hyperparameters
        self.configuracao = configuracao
        self.dimensoes = Dimensoes(configuracao.input_size, configuracao.n_actions, configuracao.hidden_size)
        self.gamma = configuracao.gamma
        # create the replay memory
        self.memory = ReplayMemory(capacity=1000)
        # create the DQN
        self.pesos = Pesos(object())
        self.dqn = DQN(self.dimensoes, self.pesos)
        # create the target DQN
        self.target_dqn = DQN(self.dimensoes, self.pesos)
        # initialize the target DQN
        self.target_dqn.load_state_dict(self.dqn.state_dict())


def _resumo(agente):
    """Hiperparametros guardados, memoria, as duas redes e a sincronia entre elas."""
    nomes = ("input_size", "n_actions", "hidden_size", "gamma",
             "batch_size", "epsilon", "epsilon_min", "epsilon_decay")
    return {
        "hiperparametros": {nome: getattr(agente.configuracao, nome) for nome in nomes},
        "memoria": (agente.memory.capacity, agente.memory.len()),
        "redes": (agente.dimensoes, agente.target_dqn.dimensoes),
        "redes_distintas": agente.dqn is not agente.target_dqn,
        "alvo_sincronizado": agente.target_dqn.state_dict()["pesos"] is agente.dqn.state_dict()["pesos"],
    }


def executar(configuracao):
    """configuracao: input_size, n_actions, hidden_size, gamma, batch_size,
    epsilon, epsilon_min e epsilon_decay."""
    c = ConfiguracaoDQN(**configuracao)
    agente = DQNAgent(c)
    return _resumo(agente)
