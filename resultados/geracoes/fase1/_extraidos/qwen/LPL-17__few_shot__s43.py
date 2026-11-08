from dataclasses import dataclass, asdict

@dataclass
class ConfiguracaoRede:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float
    lr: float = 0.001
    reduction: str = "mean"

@dataclass
class CamadaLinear:
    in_features: int
    out_features: int
    bias: bool = True

@dataclass
class ReLU:
    inplace: bool = False

@dataclass
class Sequencia:
    camadas: tuple

@dataclass
class OptimizadorAdam:
    params: list
    lr: float

@dataclass
class PerdaMSE:
    reduction: str

class DQN:
    def __init__(self, configuracao: ConfiguracaoRede):
        self.model = torch.nn.Sequential(
            torch.nn.Linear(configuracao.input_size, configuracao.hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(configuracao.hidden_size, configuracao.n_actions)
        )
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=configuracao.lr)
        self.loss_fn = torch.nn.MSELoss(reduction=configuracao.reduction)
        self.gamma = configuracao.gamma
        self.n_actions = configuracao.n_actions

def _resumo(rede):
    """Camadas em ordem, otimizador, perda e os dois valores guardados."""
    parametros = list(rede.model.parameters())
    otimizador = rede.optimizer
    mesmos = len(otimizador.params) == len(parametros) and all(
        a is b for a, b in zip(otimizador.params, parametros))
    return {
        "camadas": [camada.descricao for camada in rede.model.camadas],
        "otimizador": ("Adam", [p.formato for p in otimizador.params], otimizador.lr, mesmos),
        "perda": ("MSELoss", rede.loss_fn.reduction),
        "gamma": rede.gamma,
        "n_actions": rede.n_actions,
    }

def executar(configuracao: ConfiguracaoRede):
    """dimensoes: input_size, n_actions, hidden_size e gamma."""
    rede = DQN(configuracao)
    return _resumo(rede)
