from types import SimpleNamespace
from dataclasses import dataclass, asdict

@dataclass
class NetworkConfig:
    num_classes: int
    input_size: int
    hidden_size: int
    num_layers: int
    num_classes: int

class _Module:
    """Base of the layers: registers the assigned sublayers."""

    def __init__(self):
        self._modules = {}

    def __setattr__(self, name, value):
        if isinstance(value, _Module):
            if "_modules" not in self.__dict__:
                raise AttributeError("cannot assign module before Module.__init__() call")
            self._modules[name] = value
        object.__setattr__(self, name, value)


class _LSTM(_Module):
    """Keeps the configuration; validates size and layers like the real version."""

    def __init__(self, input_size, hidden_size, num_layers=1, bias=True, batch_first=False):
        super().__init__()
        if not isinstance(hidden_size, int):
            raise TypeError(f"hidden_size should be of type int, got: {type(hidden_size).__name__}")
        if hidden_size <= 0:
            raise ValueError("hidden_size must be greater than zero")
        if num_layers <= 0:
            raise ValueError("num_layers must be greater than zero")
        self.description = ("LSTM", input_size, hidden_size, num_layers, bias, batch_first)


class _Linear(_Module):
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.description = ("Linear", in_features, out_features, bias)


class _ReLU(_Module):
    def __init__(self, inplace=False):
        super().__init__()
        self.description = ("ReLU", inplace)


nn = SimpleNamespace(Module=_Module, LSTM=_LSTM, Linear=_Linear, ReLU=_ReLU)


class BasicLSTM(nn.Module):
    def __init__(self, config: NetworkConfig):
        super(BasicLSTM, self).__init__()
        self.config = config
        self.lstm = nn.LSTM(input_size=config.input_size, hidden_size=config.hidden_size, num_layers=config.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(config.hidden_size, 32)
        self.fc_2 = nn.Linear(32, config.num_classes)
        self.relu = nn.ReLU()


def _summary(model):
    """Hyperparameters stored in the model and the configuration of each sublayer."""
    names = ("num_classes", "input_size", "hidden_size", "num_layers")
    hyperparameters = {name: getattr(model.config, name) for name in names}
    layers = {name: layer.description for name, layer in model._modules.items()}
    return hyperparameters, layers


def run(dimensions):
    """Builds the network with the given dimensions and returns its summary. Public entry point of this unit."""
    model = BasicLSTM(NetworkConfig(**dimensions))
    return _summary(model)
