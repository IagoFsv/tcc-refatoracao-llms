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


@dataclass
class _LSTM(_Module):
    input_size: int
    hidden_size: int
    num_layers: int = 1
    bias: bool = True
    batch_first: bool = False

    def __init__(self):
        super().__init__()
        if self.hidden_size <= 0:
            raise ValueError("hidden_size must be greater than zero")
        if self.num_layers <= 0:
            raise ValueError("num_layers must be greater than zero")
        self.description = ("LSTM", self.input_size, self.hidden_size, self.num_layers, self.bias, self.batch_first)


@dataclass
class _Linear(_Module):
    in_features: int
    out_features: int
    bias: bool = True

    def __init__(self):
        super().__init__()
        self.description = ("Linear", self.in_features, self.out_features, self.bias)


@dataclass
class _ReLU(_Module):
    inplace: bool = False

    def __init__(self):
        super().__init__()
        self.description = ("ReLU", self.inplace)


nn = SimpleNamespace(Module=_Module, LSTM=_LSTM, Linear=_Linear, ReLU=_ReLU)


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
    model = BasicLSTM(
        dimensions["num_classes"],
        dimensions["input_size"],
        dimensions["hidden_size"],
        dimensions["num_layers"],
    )
    return _summary(model)
