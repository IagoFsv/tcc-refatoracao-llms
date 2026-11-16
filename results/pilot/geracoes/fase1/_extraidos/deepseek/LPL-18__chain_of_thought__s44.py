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


def executar(configuracao: AgentConfig):
    agente = DQNAgent(configuracao.input_size, configuracao.n_actions, configuracao.hidden_size, configuracao.gamma,
                      configuracao.batch_size, configuracao.epsilon, configuracao.epsilon_min, configuracao.epsilon_decay)
    return _resumo(agente)
