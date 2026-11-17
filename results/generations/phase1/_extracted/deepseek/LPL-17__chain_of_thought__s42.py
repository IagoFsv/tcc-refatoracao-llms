class Dimensions:
    def __init__(self, input_size, n_actions, hidden_size, gamma):
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma


class DQN:
    def __init__(self, dimensions):
        # define the neural network
        self.model = torch.nn.Sequential(
            torch.nn.Linear(dimensions.input_size, dimensions.hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(dimensions.hidden_size, dimensions.n_actions)
        )
        # define the optimizer
        self.optimizer = torch.optim.Adam(self.model.parameters())
        # define the loss function
        self.loss_fn = torch.nn.MSELoss()
        # define the discount factor
        self.gamma = dimensions.gamma
        self.n_actions = dimensions.n_actions


def run(input_size, n_actions, hidden_size, gamma):
    """dimensions: input_size, n_actions, hidden_size and gamma. Public entry point of this unit."""
    dimensions = Dimensions(input_size, n_actions, hidden_size, gamma)
    network = DQN(dimensions)
    return _summary(network)
