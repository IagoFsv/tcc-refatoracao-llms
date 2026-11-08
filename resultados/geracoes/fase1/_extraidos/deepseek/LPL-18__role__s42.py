class Params:
    def __init__(self, input_size, n_actions, hidden_size, gamma, batch_size, epsilon, epsilon_min, epsilon_decay):
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma
        self.batch_size = batch_size
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay


class DQN:
    """Rede minima: dimensoes recebidas e pesos copiaveis."""

    def __init__(self, params: Params):
        if min(params.input_size, params.n_actions, params.hidden_size) < 0:
            raise RuntimeError("Trying to create tensor with negative dimension")
        self.params = params
        self.pesos = {"pesos": object()}

    def state_dict(self):
        return dict(self.pesos)

    def load_state_dict(self, state_dict):
        self.pesos = dict(state_dict)


class DQNAgent:
    def __init__(self, params: Params):
        # define the hyperparameters
        self.params = params
        # create the replay memory
        self.memory = ReplayMemory(capacity=1000)
        # create the DQN
        self.dqn = DQN(params)
        # create the target DQN
        self.target_dqn = DQN(params)
        # initialize the target DQN
        self.target_dqn.load_state_dict(self.dqn.state_dict())


def executar(configuracao):
    """configuracao: input_size, n_actions, hidden_size, gamma, batch_size,
    epsilon, epsilon_min e epsilon_decay."""
    c = Params(**configuracao)
    agente = DQNAgent(c)
    return _resumo(agente)
