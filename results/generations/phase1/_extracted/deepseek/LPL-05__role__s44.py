from types import SimpleNamespace


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
    def __init__(self, config):
        super().__init__()
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
        self.config = config
        self.lstm = nn.LSTM(input_size=config.input_size, hidden_size=config.hidden_size, num_layers=config.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(config.hidden_size, 32)
        self.fc_2 = nn.Linear(32, config.num_classes)
        self.relu = nn.ReLU()


def _summary(model):
    names = ("num_classes", "input_size", "hidden_size", "num_layers")
    hyperparameters = {name: getattr(model.config, name) for name in names}
    layers = {name: layer.description for name, layer in model._modules.items()}
    return hyperparameters, layers


def run(dimensions):
    config = SimpleNamespace(**dimensions)
    model = BasicLSTM(config)
    return _summary(model)
