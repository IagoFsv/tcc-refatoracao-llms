from dataclasses import dataclass, asdict

@dataclass
class DQNConfig:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float

def executar(config: DQNConfig):
    rede = DQN(config.input_size, config.n_actions, config.hidden_size, config.gamma)
    return _resumo(rede)

def _resumo(rede):
    """Camadas em ordem, otimizador, perda e os dois valores guardados."""
    parametros = list(rede.model.parameters())
    otimizador = rede.optimizer
    mesmos = len(otimizador.params) == len(parametros) and all(a is b for a, b in zip(otimizador.params, parametros))
    return {
        "camadas": [camada.descricao for camada in rede.model.camadas],
        "otimizador": ("Adam", [p.formato for p in otimizador.params], otimizador.lr, mesmos),
        "perda": ("MSELoss", rede.loss_fn.reduction),
        "gamma": rede.gamma,
        "n_actions": rede.n_actions,
    }
