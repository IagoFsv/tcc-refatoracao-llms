class AgentConfig:
    def __init__(self, input_size, n_actions, hidden_size, gamma, batch_size, epsilon, epsilon_min, epsilon_decay):
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma
        self.batch_size = batch_size
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

class DQNAgent:
    def __init__(self, config: AgentConfig):
         # define the hyperparameters
        self.config = config
        # create the replay memory
        self.memory = ReplayMemory(capacity=1000)
        # create the DQN
        self.dqn = DQN(self.config.input_size, self.config.n_actions, self.config.hidden_size, self.config.gamma)
        # create the target DQN
        self.target_dqn = DQN(self.config.input_size, self.config.n_actions, self.config.hidden_size, self.config.gamma)
        # initialize the target DQN
        self.target_dqn.load_state_dict(self.dqn.state_dict())

def run(configuration):
    """Public entry point of this unit.
    configuration: input_size, n_actions, hidden_size, gamma, batch_size,
    epsilon, epsilon_min and epsilon_decay.
    """
    c = AgentConfig(**configuration)
    agent = DQNAgent(c)
    return _summary(agent)
