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

class DQNAgent:
    def __init__(self, configuracao: Configuracao):
        self.configuracao = configuracao
        self.memory = ReplayMemory(capacity=1000)
        self.dqn = DQN(*configuracao)
        self.target_dqn = DQN(*configuracao)
        self.target_dqn.load_state_dict(self.dqn.state_dict())

def executar(configuracao: Configuracao):
    agente = DQNAgent(configuracao)
    return _resumo(agente)
