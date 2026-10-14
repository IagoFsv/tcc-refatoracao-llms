"""Rede recorrente para classificar a proxima letra de um nome.

Ponto de entrada publico: executar(dimensoes). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.

As camadas (modulo base, LSTM, linear, ReLU) sao versoes minimas que so
guardam a configuracao recebida. O modulo base registra cada subcamada
atribuida, pelo nome do atributo, e recusa subcamada atribuida antes da
inicializacao da classe base.
"""

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
	def __init__(self, num_classes, input_size, hidden_size, num_layers):
		# github copilot suggestion
		super(BasicLSTM, self).__init__()
		self.num_classes = num_classes
		self.num_layers = num_layers
		self.input_size = input_size
		self.hidden_size = hidden_size
		# I figure we will need this one, should be 27 for alpahebet plus EOS
		# self.seq_length = 27
		self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
		# self.fc_1 = nn.Linear(hidden_size, 64)
		# self.fc_2 = nn.Linear(64, num_classes)
		# starting with a smaller number of nodes to keep training time down
		self.fc_1 = nn.Linear(hidden_size, 32)
		self.fc_2 = nn.Linear(32, num_classes)

		# this one wasn't suggested by copilot, not needed? a ReLu can't hurt though..
		self.relu = nn.ReLU()


def _resumo(modelo):
    """Hiperparametros guardados no modelo e configuracao de cada subcamada."""
    nomes = ("num_classes", "input_size", "hidden_size", "num_layers")
    hiperparametros = {nome: getattr(modelo, nome) for nome in nomes}
    camadas = {nome: camada.descricao for nome, camada in modelo._camadas.items()}
    return hiperparametros, camadas


def executar(dimensoes):
    """Monta a rede com as dimensoes dadas e devolve o resumo dela."""
    modelo = BasicLSTM(
        dimensoes["num_classes"],
        dimensoes["input_size"],
        dimensoes["hidden_size"],
        dimensoes["num_layers"],
    )
    return _resumo(modelo)
