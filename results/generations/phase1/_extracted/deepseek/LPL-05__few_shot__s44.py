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
    def __init__(self, params: dict):
        super().__init__()
        if not isinstance(params['hidden_size'], int):
            raise TypeError(f"hidden_size should be of type int, got: {type(params['hidden_size']).__name__}")
        if params['hidden_size'] <= 0:
            raise ValueError("hidden_size must be greater than zero")
        if params['num_layers'] <= 0:
            raise ValueError("num_layers must be greater than zero")
        self.description = ("LSTM", params['input_size'], params['hidden_size'], params['num_layers'], params['bias'], params['batch_first'])


class _Linear(_Module):
    def __init__(self, params: dict):
        super().__init__()
        self.description = ("Linear", params['in_features'], params['out_features'], params['bias'])


class _ReLU(_Module):
    def __init__(self, params: dict):
        super().__init__()
        self.description = ("ReLU", params['inplace'])


nn = SimpleNamespace(Module=_Module, LSTM=_LSTM, Linear=_Linear, ReLU=_ReLU)

@dataclass
class BasicLSTMParams:
    num_classes: int
    input_size: int
    hidden_size: int
    num_layers: int

class BasicLSTM(nn.Module):
    def __init__(self, params: BasicLSTMParams):
        super(BasicLSTM, self).__init__()
        self.params = params
        self.lstm = nn.LSTM(input_size=params.input_size, hidden_size=params.hidden_size, num_layers=params.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(self.params.hidden_size, 32)
        self.fc_2 = nn.Linear(32, self.params.num_classes)
        self.relu = nn.ReLU()


def _summary(model):
    names = ("num_classes", "input_size", "hidden_size", "num_layers")
    hyperparameters = {name: getattr(model.params, name) for name in names}
    layers = {name: layer.description for name, layer in model._modules.items()}
    return hyperparameters, layers


def run(dimensions: dict):
    params = BasicLSTMParams(**dimensions)
    model = BasicLSTM(params)
    return _summary(model)
