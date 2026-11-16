from dataclasses import dataclass, asdict

@dataclass
class ConfiguracaoRede:
    num_classes: int
    input_size: int
    hidden_size: int
    num_layers: int

class BasicLSTM(nn.Module):
    def __init__(self, configuracao: ConfiguracaoRede):
        super(BasicLSTM, self).__init__()
        self.num_classes = configuracao.num_classes
        self.num_layers = configuracao.num_layers
        self.input_size = configuracao.input_size
        self.hidden_size = configuracao.hidden_size
        self.lstm = nn.LSTM(input_size=configuration.input_size, hidden_size=configuration.hidden_size, num_layers=configuration.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(configuration.hidden_size, 32)
        self.fc_2 = nn.Linear(32, configuration.num_classes)
        self.relu = nn.ReLU()

def _resumo(modelo):
    nomes = ("num_classes", "input_size", "hidden_size", "num_layers")
    hiperparametros = {nome: getattr(modelo, nome) for nome in nomes}
    camadas = {nome: camada.descricao for nome, camada in modelo._camadas.items()}
    return hiperparametros, camadas

def executar(configuracao: ConfiguracaoRede):
    modelo = BasicLSTM(configuracao)
    return _resumo(modelo)
