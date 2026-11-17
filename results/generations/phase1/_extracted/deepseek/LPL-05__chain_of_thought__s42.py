class LSTMParameters:
    def __init__(self, num_classes, input_size, hidden_size, num_layers):
        self.num_classes = num_classes
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers


class BasicLSTM(nn.Module):
    def __init__(self, lstm_params: LSTMParameters):
        super(BasicLSTM, self).__init__()
        self.lstm_params = lstm_params
        self.lstm = nn.LSTM(input_size=lstm_params.input_size, hidden_size=lstm_params.hidden_size, 
                            num_layers=lstm_params.num_layers, batch_first=True)
        self.fc_1 = nn.Linear(lstm_params.hidden_size, 32)
        self.fc_2 = nn.Linear(32, lstm_params.num_classes)
        self.relu = nn.ReLU()


def run(dimensions):
    lstm_params = LSTMParameters(dimensions["num_classes"], dimensions["input_size"], 
                                 dimensions["hidden_size"], dimensions["num_layers"])
    model = BasicLSTM(lstm_params)
    return _summary(model)
