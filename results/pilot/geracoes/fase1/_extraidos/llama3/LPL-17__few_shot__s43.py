from dataclasses import dataclass, asdict

@dataclass
class Dimensoes:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float

def executar(dimensoes: Dimensoes):
    rede = DQN(dimensoes.input_size, dimensoes.n_actions, dimensoes.hidden_size, dimensoes.gamma)
    return _resumo(rede)
