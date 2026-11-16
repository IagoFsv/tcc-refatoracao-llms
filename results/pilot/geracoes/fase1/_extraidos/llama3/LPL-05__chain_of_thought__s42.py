class ModeloConfig:
    def __init__(self, num_classes, input_size, hidden_size, num_layers):
        self.num_classes = num_classes
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers

def executar(config):
    modelo = BasicLSTM(config.num_classes, config.input_size, config.hidden_size, config.num_layers)
    return _resumo(modelo)
