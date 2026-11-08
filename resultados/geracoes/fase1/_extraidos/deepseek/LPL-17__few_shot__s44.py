from dataclasses import dataclass, asdict

@dataclass
class Parameters:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float

def execute(parameters: Parameters):
    rede = DQN(parameters.input_size, parameters.n_actions,
               parameters.hidden_size, parameters.gamma)
    return _resumo(rede)
