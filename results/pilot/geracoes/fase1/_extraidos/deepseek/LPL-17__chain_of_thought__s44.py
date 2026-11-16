class Parameters:
    def __init__(self, input_size, n_actions, hidden_size, gamma):
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma

class DQN:
    def __init__(self, parameters: Parameters):
        # define the neural network
        self.model = torch.nn.Sequential(
            torch.nn.Linear(parameters.input_size, parameters.hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(parameters.hidden_size, parameters.n_actions)
        )
        # define the optimizer
        self.optimizer = torch.optim.Adam(self.model.parameters())
        # define the loss function
        self.loss_fn = torch.nn.MSELoss()
        # define the discount factor
        self.gamma = parameters.gamma
        self.n_actions = parameters.n_actions

def executar(dimensoes):
    parameters = Parameters(dimensoes["input_size"], dimensoes["n_actions"],
                            dimensoes["hidden_size"], dimensoes["gamma"])
    rede = DQN(parameters)
    return _resumo(rede)
