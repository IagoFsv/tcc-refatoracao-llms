from dataclasses import dataclass, asdict

@dataclass
class Dimensions:
    num_classes: int
    input_size: int
    hidden_size: int
    num_layers: int

class BasicLSTM(nn.Module):
    def __init__(self, dimensions: Dimensions):
        super(BasicLSTM, self).__init__()
        self.dimensions = dimensions
        self.lstm = nn.LSTM(input_size=self.dimensions.input_size, hidden_size=self.dimensions.hidden_size, num_layers=self.dimensions.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(self.dimensions.hidden_size, 32)
        self.fc_2 = nn.Linear(32, self.dimensions.num_classes)
        self.relu = nn.ReLU()

def execute(dimensions: Dimensions):
    model = BasicLSTM(dimensions)
    return _resumo(model)
