from types import SimpleNamespace


class _Modulo:
    """Base das camadas: registra as subcamadas atribuidas."""

    def __init__(self):
        self._camadas = {}

    def __setattr__(self, nome, valor):
        if isinstance(valor, _Modulo):
            if "_camadas" not in self.__dict__:
                raise AttributeError("cannot assign module before Module.__init__() call")
            self._camadas[nome] = valor
        object.__setattr__(self, nome, valor)


class _LSTM(_Modulo):
    """Guarda a configuracao; valida tamanho e camadas como a versao real."""

    def __init__(self, input_size, hidden_size, num_layers=1, bias=True, batch_first=False):
        super().__init__()
        if not isinstance(hidden_size, int):
            raise TypeError(f"hidden_size should be of type int, got: {type(hidden_size).__name__}")
        if hidden_size <= 0:
            raise ValueError("hidden_size must be greater than zero")
        if num_layers <= 0:
            raise ValueError("num_layers must be greater than zero")
        self.descricao = ("LSTM", input_size, hidden_size, num_layers, bias, batch_first)


class _Linear(_Modulo):
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.descricao = ("Linear", in_features, out_features, bias)


class _ReLU(_Modulo):
    def __init__(self, inplace=False):
        super().__init__()
        self.descricao = ("ReLU", inplace)


nn = SimpleNamespace(Module=_Modulo, LSTM=_LSTM, Linear=_Linear, ReLU=_ReLU)


class BasicLSTM(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.lstm = nn.LSTM(**config.lstm)
        self.fc_1 = nn.Linear(**config.fc_1)
        self.fc_2 = nn.Linear(**config.fc_2)
        self.relu = nn.ReLU()


def _resumo(modelo):
    """Hiperparametros guardados no modelo e configuracao de cada subcamada."""
    nomes = ("num_classes", "input_size", "hidden_size", "num_layers")
    hiperparametros = {nome: getattr(modelo.config, nome) for nome in nomes}
    camadas = {nome: camada.descricao for nome, camada in modelo._camadas.items()}
    return hiperparametros, camadas


def executar(config):
    """Monta a rede com as dimensoes dadas e devolve o resumo dela."""
    modelo = BasicLSTM(config)
    return _resumo(modelo)

config = {
    "num_classes": 27,
    "input_size": 27,
    "hidden_size": 32,
    "num_layers": 1,
    "lstm": {"input_size": 27, "hidden_size": 32, "num_layers": 1, "batch_first": True},
    "fc_1": {"in_features": 32, "out_features": 32},
    "fc_2": {"in_features": 32, "out_features": 27}
}

print(executar(config))
