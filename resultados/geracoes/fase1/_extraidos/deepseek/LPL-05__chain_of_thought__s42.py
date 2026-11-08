class Dimensions:
    def __init__(self, num_classes, input_size, hidden_size, num_layers):
        self.num_classes = num_classes
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers


class BasicLSTM(nn.Module):
    def __init__(self, dimensions: Dimensions):
        super(BasicLSTM, self).__init__()
        self.dimensions = dimensions
        self.lstm = nn.LSTM(input_size=dimensions.input_size, hidden_size=dimensions.hidden_size, 
                            num_layers=dimensions.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(dimensions.hidden_size, 32)
        self.fc_2 = nn.Linear(32, dimensions.num_classes)
        self.relu = nn.ReLU()


def executar(dimensions: Dimensions):
    model = BasicLSTM(dimensions)
    return _resumo(model)
