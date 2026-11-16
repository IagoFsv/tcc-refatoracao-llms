from types import SimpleNamespace


class Module:
    def __init__(self):
        self._layers = {}

    def __setattr__(self, name, value):
        if isinstance(value, Module):
            if "_layers" not in self.__dict__:
                raise AttributeError("cannot assign module before Module.__init__() call")
            self._layers[name] = value
        super().__setattr__(name, value)


class LSTM(Module):
    def __init__(self, input_size, hidden_size, num_layers=1, bias=True, batch_first=False):
        super().__init__()
        if not isinstance(hidden_size, int):
            raise TypeError(f"hidden_size should be of type int, got: {type(hidden_size).__name__}")
        if hidden_size <= 0:
            raise ValueError("hidden_size must be greater than zero")
        if num_layers <= 0:
            raise ValueError("num_layers must be greater than zero")
        self.description = ("LSTM", input_size, hidden_size, num_layers, bias, batch_first)


class Linear(Module):
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.description = ("Linear", in_features, out_features, bias)


class ReLU(Module):
    def __init__(self, inplace=False):
        super().__init__()
        self.description = ("ReLU", inplace)


nn = SimpleNamespace(Module=Module, LSTM=LSTM, Linear=Linear, ReLU=ReLU)


class BasicLSTM(nn.Module):
    def __init__(self, num_classes, input_size, hidden_size, num_layers):
        super().__init__()
        self.num_classes = num_classes
        self.num_layers = num_layers
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.fc_1 = nn.Linear(hidden_size, 32)
        self.fc_2 = nn.Linear(32, num_classes)
        self.relu = nn.ReLU()


def summary(model):
    names = ("num_classes", "input_size", "hidden_size", "num_layers")
    hyperparameters = {name: getattr(model, name) for name in names}
    layers = {name: layer.description for name, layer in model._layers.items()}
    return hyperparameters, layers


def execute(dimensions):
    model = BasicLSTM(
        dimensions["num_classes"],
        dimensions["input_size"],
        dimensions["hidden_size"],
        dimensions["num_layers"],
    )
    return summary(model)
