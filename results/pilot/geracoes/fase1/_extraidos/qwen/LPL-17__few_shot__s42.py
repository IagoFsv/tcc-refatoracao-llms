from dataclasses import dataclass, asdict

@dataclass
class RedesNeuraisConfig:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float
    optim_lr: float = 0.001
    loss_reduction: str = "mean"

@dataclass
class CamadaLinearConfig:
    in_features: int
    out_features: int
    bias: bool = True

@dataclass
class ReLUConfig:
    inplace: bool = False

@dataclass
class SequentialConfig:
    camadas: list

@dataclass
class AdamConfig:
    params: list
    lr: float = 0.001

@dataclass
class MSELossConfig:
    reduction: str = "mean"

class DQNConfig:
    redes_neurais: RedesNeuraisConfig
    camada_linear: CamadaLinearConfig
    relu: ReLUConfig
    sequencial: SequentialConfig
    adam: AdamConfig
    mseloss: MSELossConfig

class DQN:
    def __init__(self, config: DQNConfig):
        # define the neural network
        self.model = torch.nn.Sequential(
            torch.nn.Linear(config.camada_linear.in_features, config.camada_linear.out_features),
            torch.nn.ReLU(),
            torch.nn.Linear(config.camada_linear.out_features, config.redes_neurais.n_actions)
        )
        # define the optimizer
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=config.adam.lr)
        # define the loss function
        self.loss_fn = torch.nn.MSELoss(reduction=config.mseloss.reduction)
        # define the discount factor
        self.gamma = config.redes_neurais.gamma
        self.n_actions = config.redes_neurais.n_actions

def _resumo(config: DQNConfig):
    """Camadas em ordem, otimizador, perda e os dois valores guardados."""
    parametros = list(config.model.parameters())
    otimizador = config.optimizer
    mesmos = len(otimizador.params) == len(parametros) and all(
        a is b for a, b in zip(otimizador.params, parametros))
    return {
        "camadas": [camada.descricao for camada in config.model.camadas],
        "otimizador": ("Adam", [p.formato for p in otimizador.params], otimizador.lr, mesmos),
        "perda": ("MSELoss", config.loss_fn.reduction),
        "gamma": config.redes_neurais.gamma,
        "n_actions": config.redes_neurais.n_actions,
    }

def executar(config: DQNConfig):
    """dimensoes: input_size, n_actions, hidden_size e gamma."""
    rede = DQN(config)
    return _resumo(config)
