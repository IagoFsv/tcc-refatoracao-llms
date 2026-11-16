class Config:
    def __init__(self, num_classes, input_size, hidden_size, num_layers):
        self.num_classes = num_classes
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers

class BasicLSTM(nn.Module):
    def __init__(self, config):
        super(BasicLSTM, self).__init__()
        self.config = config
        self.lstm = nn.LSTM(input_size=config.input_size, hidden_size=config.hidden_size, num_layers=config.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(config.hidden_size, 32)
        self.fc_2 = nn.Linear(32, config.num_classes)
        self.relu = nn.ReLU()

def _resumo(modelo):
    nomes = ("num_classes", "input_size", "hidden_size", "num_layers")
    hiperparametros = {nome: getattr(modelo, nome) for nome in nomes}
    camadas = {nome: camada.descricao for nome, camada in modelo._camadas.items()}
    return hiperparametros, camadas

def executar(config):
    modelo = BasicLSTM(config)
    return _resumo(modelo)
