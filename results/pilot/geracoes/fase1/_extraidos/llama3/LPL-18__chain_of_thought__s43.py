class Config:
    def __init__(self, input_size, n_actions, hidden_size, gamma, batch_size, epsilon, epsilon_min, epsilon_decay):
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma
        self.batch_size = batch_size
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

def executar(config):
    agente = DQNAgent(config.input_size, config.n_actions, config.hidden_size, config.gamma,
                      config.batch_size, config.epsilon, config.epsilon_min, config.epsilon_decay)
    return _resumo(agente)

# Exemplo de uso:
config = Config(10, 2, 128, 0.9, 32, 0.1, 0.01, 0.99)
result = executar(config)
