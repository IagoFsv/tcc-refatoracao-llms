"""Recurrent network to classify the next letter of a name.

Public entry point: run(dimensions). Do not change its name or signature; the
rest of the file may be freely reorganized.

The layers (base module, LSTM, linear, ReLU) are minimal versions that only
keep the configuration they receive. The base module registers each assigned
sublayer by attribute name, and refuses a sublayer assigned before the base
class is initialized.
"""

from types import SimpleNamespace


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

    def __init__(self, config):
        super().__init__()
        if not isinstance(config.hidden_size, int):
            raise TypeError(f"hidden_size should be of type int, got: {type(config.hidden_size).__name__}")
        if config.hidden_size <= 0:
            raise ValueError("hidden_size must be greater than zero")
        if config.num_layers <= 0:
            raise ValueError("num_layers must be greater than zero")
        self.description = ("LSTM", config.input_size, config.hidden_size, config.num_layers, config.bias, config.batch_first)


class _Linear(_Module):
    def __init__(self, config):
        super().__init__()
        self.description = ("Linear", config.in_features, config.out_features, config.bias)


class _ReLU(_Module):
    def __init__(self, config):
        super().__init__()
        self.description = ("ReLU", config.inplace)


nn = SimpleNamespace(Module=_Module, LSTM=_LSTM, Linear=_Linear, ReLU=_ReLU)


class BasicLSTM(nn.Module):
    def __init__(self, config):
        super(BasicLSTM, self).__init__()
        self.num_classes = config.num_classes
        self.num_layers = config.num_layers
        self.input_size = config.input_size
        self.hidden_size = config.hidden_size
        self.lstm = nn.LSTM(input_size=config.input_size, hidden_size=config.hidden_size, num_layers=config.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(hidden_size=config.hidden_size, out_features=32)
        self.fc_2 = nn.Linear(32, config.num_classes)
        self.relu = nn.ReLU()


def _summary(model):
    """Hyperparameters stored in the model and the configuration of each sublayer."""
    names = ("num_classes", "input_size", "hidden_size", "num_layers")
    hyperparameters = {name: getattr(model, name) for name in names}
    layers = {name: layer.description for name, layer in model._modules.items()}
    return hyperparameters, layers


def run(dimensions):
    """Builds the network with the given dimensions and returns its summary. Public entry point of this unit."""
    config = SimpleNamespace(
        num_classes=dimensions["num_classes"],
        input_size=dimensions["input_size"],
        hidden_size=dimensions["hidden_size"],
        num_layers=dimensions["num_layers"],
        bias=True,
        batch_first=True,
        in_features=dimensions["input_size"],
        out_features=32,
        inplace=False
    )
    model = BasicLSTM(config)
    return _summary(model)
