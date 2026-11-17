class BasicLSTMParams:
    def __init__(self, num_classes, input_size, hidden_size, num_layers):
        self.num_classes = num_classes
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers

class BasicLSTM(nn.Module):
    def __init__(self, params: BasicLSTMParams):
        super(BasicLSTM, self).__init__()
        self.params = params
        self.lstm = nn.LSTM(input_size=params.input_size, hidden_size=params.hidden_size, num_layers=params.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(params.hidden_size, 32)
        self.fc_2 = nn.Linear(32, params.num_classes)
        self.relu = nn.ReLU()

def run(dimensions):
    params = BasicLSTMParams(
        dimensions["num_classes"],
        dimensions["input_size"],
        dimensions["hidden_size"],
        dimensions["num_layers"],
    )
    model = BasicLSTM(params)
    return _summary(model)
