class Parameters:
    def __init__(self, num_classes, input_size, hidden_size, num_layers):
        self.num_classes = num_classes
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers

class BasicLSTM(nn.Module):
    def __init__(self, parameters: Parameters):
        super(BasicLSTM, self).__init__()
        self.parameters = parameters
        self.lstm = nn.LSTM(input_size=parameters.input_size, hidden_size=parameters.hidden_size, num_layers=parameters.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(parameters.hidden_size, 32)
        self.fc_2 = nn.Linear(32, parameters.num_classes)
        self.relu = nn.ReLU()

def run(dimensions):
    parameters = Parameters(dimensions["num_classes"], dimensions["input_size"], dimensions["hidden_size"], dimensions["num_layers"])
    model = BasicLSTM(parameters)
    return _summary(model)
