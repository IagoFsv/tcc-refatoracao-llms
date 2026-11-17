from types import SimpleNamespace
from dataclasses import dataclass, asdict

class _Module:
    def __init__(self):
        self._modules = {}

    def __setattr__(self, name, value):
        if isinstance(value, _Module):
            if "_modules" not in self.__dict__:
                raise AttributeError("cannot assign module before Module.__init__() call")
            self._modules[name] = value
        object.__setattr__(self, name, value)


class _LSTM(_Module):
    def __init__(self, config: dict):
        super().__init__()
        self.description = ("LSTM", asdict(config))


class _Linear(_Module):
    def __init__(self, config: dict):
        super().__init__()
        self.description = ("Linear", asdict(config))


class _ReLU(_Module):
    def __init__(self, config: dict):
        super().__init__()
        self.description = ("ReLU", asdict(config))


nn = SimpleNamespace(Module=_Module, LSTM=_LSTM, Linear=_Linear, ReLU=_ReLU)


@dataclass
class LSTMConfig:
    input_size: int
    hidden_size: int
    num_layers: int
    bias: bool
    batch_first: bool


@dataclass
class LinearConfig:
    in_features: int
    out_features: int
    bias: bool


@dataclass
class ReLUConfig:
    inplace: bool


class BasicLSTM(nn.Module):
    def __init__(self, num_classes, input_size, hidden_size, num_layers):
        super(BasicLSTM, self).__init__()
        self.num_classes = num_classes
        self.num_layers = num_layers
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.fc_1 = nn.Linear(hidden_size, 32)
        self.fc_2 = nn.Linear(32, num_classes)
        self.relu = nn.ReLU()


def _summary(model):
    names = ("num_classes", "input_size", "hidden_size", "num_layers")
    hyperparameters = {name: getattr(model, name) for name in names}
    layers = {name: layer.description for name, layer in model._modules.items()}
    return hyperparameters, layers


def run(dimensions):
    lstm_config = LSTMConfig(
        dimensions["input_size"],
        dimensions["hidden_size"],
        dimensions["num_layers"],
        True,
        True
    )
    linear_config = LinearConfig(
        dimensions["hidden_size"],
        dimensions["num_classes"],
        True
    )
    relu_config = ReLUConfig(False)

    model = BasicLSTM(
        dimensions["num_classes"],
        dimensions["input_size"],
        dimensions["hidden_size"],
        dimensions["num_layers"],
    )
    model.lstm = nn.LSTM(**asdict(lstm_config))
    model.fc_1 = nn.Linear(**asdict(linear_config))
    model.fc_2 = nn.Linear(**asdict(linear_config))
    model.relu = nn.ReLU(**asdict(relu_config))
    return _summary(model)
