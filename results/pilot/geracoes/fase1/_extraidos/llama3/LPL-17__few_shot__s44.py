from dataclasses import dataclass

@dataclass
class Rede:
    input_size: int
    n_actions: int
    hidden_size: int
    gamma: float

    def __init__(self, input_size, n_actions, hidden_size, gamma):
        self.model = torch.nn.Sequential(
            torch.nn.Linear(input_size, hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_size, n_actions)
        )
        self.optimizer = torch.optim.Adam(self.model.parameters())
        self.loss_fn = torch.nn.MSELoss()
        self.gamma = gamma
        self.n_actions = n_actions

    def parametros(self):
        return list(self.model.parameters())

    def __str__(self):
        return f"Rede({self.input_size}, {self.n_actions}, {self.hidden_size}, {self.gamma})"


def _resumo(rede):
    """Camadas em ordem, otimizador, perda e os dois valores guardados."""
    return {
        "camadas": [camada.descricao for camada in rede.model.camadas],
        "otimizador": ("Adam", [p.formato for p in rede.optimizer.params], rede.optimizer.lr),
        "perda": ("MSELoss", rede.loss_fn.reduction),
        "gamma": rede.gamma,
        "n_actions": rede.n_actions,
    }


def executar(dimensoes: Rede):
    return _resumo(dimensoes)
