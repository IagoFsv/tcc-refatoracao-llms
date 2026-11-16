from dataclasses import dataclass, asdict

@dataclass
class Configuracao:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float
    batch_size: int
    epsilon: float
    epsilon_min: float
    epsilon_decay: float

@dataclass
class Rede:
    dimensoes: tuple
    pesos: dict

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
    def __init__(self, configuracao: Configuracao):
        self.configuracao = configuracao
        self.dqn = Rede(self.configuracao.input_size, self.configuracao.n_actions, self.configuracao.hidden_size, self.configuracao.gamma)
        self.target_dqn = Rede(self.configuracao.input_size, self.configuracao.n_actions, self.configuracao.hidden_size, self.configuracao.gamma)
        self.memory = ReplayMemory(capacity=1000)
        self.target_dqn.load_state_dict(self.dqn.state_dict())

def _resumo(agente: DQNAgent):
    return {
        "hiperparametros": asdict(agente.configuracao),
        "memoria": (agente.memory.capacity, agente.memory.len()),
        "redes": (agente.dqn.dimensoes, agente.target_dqn.dimensoes),
        "redes_distintas": agente.dqn is not agente.target_dqn,
        "alvo_sincronizado": agente.target_dqn.state_dict()["pesos"] is agente.dqn.state_dict()["pesos"],
    }

def executar(configuracao: Configuracao):
    agente = DQNAgent(configuracao)
    return _resumo(agente)
