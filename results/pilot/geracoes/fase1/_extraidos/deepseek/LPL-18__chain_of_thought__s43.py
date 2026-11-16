class AgentParameters:
    def __init__(self, input_size, n_actions, hidden_size, gamma, batch_size, epsilon, epsilon_min, epsilon_decay):
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma
        self.batch_size = batch_size
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

def executar(configuracao):
    # Cria um novo objeto AgentParameters com os parâmetros de configuração
    agent_params = AgentParameters(**configuracao)
    # Cria um novo objeto DQNAgent com os parâmetros do agente
    agente = DQNAgent(agent_params.input_size, agent_params.n_actions, agent_params.hidden_size, agent_params.gamma,
                      agent_params.batch_size, agent_params.epsilon, agent_params.epsilon_min, agent_params.epsilon_decay)
    return _resumo(agente)
