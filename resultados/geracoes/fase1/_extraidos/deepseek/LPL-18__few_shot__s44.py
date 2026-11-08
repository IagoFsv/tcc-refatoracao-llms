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

@dataclass
class DQNAgent:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float
    batch_size: int
    epsilon: float
    epsilon_min: float
    epsilon_decay: float
    memory: ReplayMemory
    dqn: Rede
    target_dqn: Rede

def _resumo(agente: DQNAgent):
    nomes = ("input_size", "n_actions", "hidden_size", "gamma",
             "batch_size", "epsilon", "epsilon_min", "epsilon_decay")
    return {
        "hiperparametros": {nome: getattr(agente, nome) for nome in nomes},
        "memoria": (agente.memory.capacity, agente.memory.len()),
        "redes": (agente.dqn.dimensoes, agente.target_dqn.dimensoes),
        "redes_distintas": agente.dqn is not agente.target_dqn,
        "alvo_sincronizado": agente.target_dqn.pesos == agente.dqn.pesos,
    }

def executar(configuracao: Configuracao):
    agente = DQNAgent(
        configuracao.input_size, 
        configuracao.n_actions, 
        configuracao.hidden_size, 
        configuracao.gamma,
        configuracao.batch_size, 
        configuracao.epsilon, 
        configuracao.epsilon_min, 
        configuracao.epsilon_decay,
        ReplayMemory(capacity=1000),
        Rede((configuracao.input_size, configuracao.n_actions, configuracao.hidden_size, configuracao.gamma), {"pesos": object()}),
        Rede((configuracao.input_size, configuracao.n_actions, configuracao.hidden_size, configuracao.gamma), {"pesos": object()})
    )
    return _resumo(agente)
