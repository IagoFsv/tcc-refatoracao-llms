from dataclasses import dataclass, asdict

@dataclass
class ConfiguracaoLSTM:
    input_size: int
    hidden_size: int
    num_layers: int = 1
    bias: bool = True
    batch_first: bool = False


@dataclass
class ConfiguracaoLinear:
    in_features: int
    out_features: int
    bias: bool = True


@dataclass
class ConfiguracaoReLU:
    inplace: bool = False


@dataclass
class Dimensoes:
    num_classes: int
    input_size: int
    hidden_size: int
    num_layers: int


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

    def __init__(self, configuracao: ConfiguracaoLSTM):
        super().__init__()
        self.descricao = configuracao


class _Linear(_Modulo):
    def __init__(self, configuracao: ConfiguracaoLinear):
        super().__init__()
        self.descricao = configuracao


class _ReLU(_Modulo):
    def __init__(self, configuracao: ConfiguracaoReLU):
        super().__init__()
        self.descricao = configuracao


nn = SimpleNamespace(Module=_Modulo, LSTM=_LSTM, Linear=_Linear, ReLU=_ReLU)


class BasicLSTM(nn.Module):
    def __init__(self, configuracao: Dimensoes):
        super(BasicLSTM, self).__init__()
        self.num_classes = configuracao.num_classes
        self.num_layers = configuracao.num_layers
        self.input_size = configuracao.input_size
        self.hidden_size = configuracao.hidden_size
        self.lstm = nn.LSTM(input_size=configuracao.input_size, hidden_size=configuracao.hidden_size, num_layers=configuracao.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(configuracao.hidden_size, 32)
        self.fc_2 = nn.Linear(32, configuracao.num_classes)
        self.relu = nn.ReLU()


def _resumo(modelo):
    nomes = ("num_classes", "input_size", "hidden_size", "num_layers")
    hiperparametros = {nome: getattr(modelo, nome) for nome in nomes}
    camadas = {nome: camada.descricao for nome, camada in modelo._camadas.items()}
    return hiperparametros, camadas


def executar(dimensoes: Dimensoes):
    modelo = BasicLSTM(dimensoes)
    return _resumo(modelo)
