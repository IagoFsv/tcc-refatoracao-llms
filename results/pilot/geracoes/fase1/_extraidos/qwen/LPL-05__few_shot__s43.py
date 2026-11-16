from dataclasses import dataclass, asdict

@dataclass
class Configuracao:
    num_classes: int
    input_size: int
    hidden_size: int
    num_layers: int

@dataclass
class BasicLSTM(nn.Module):
    def __init__(self, configuracao: Configuracao):
        super(BasicLSTM, self).__init__()
        self.num_classes = configuracao.num_classes
        self.num_layers = configuracao.num_layers
        self.input_size = configuracao.input_size
        self.hidden_size = configuracao.hidden_size
        self.lstm = nn.LSTM(input_size=configuracao.input_size, hidden_size=configuracao.hidden_size, num_layers=configuracao.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(configuracao.hidden_size, 32)
        self.fc_2 = nn.Linear(32, configuracao.num_classes)
        self.relu = nn.ReLU()

def _resumo(modelo: BasicLSTM):
    nomes = ("num_classes", "input_size", "hidden_size", "num_layers")
    hiperparametros = {nome: getattr(modelo, nome) for nome in nomes}
    camadas = {nome: camada.descricao for nome, camada in modelo._camadas.items()}
    return hiperparametros, camadas

def executar(configuracao: Configuracao):
    modelo = BasicLSTM(configuracao)
    return _resumo(modelo)
