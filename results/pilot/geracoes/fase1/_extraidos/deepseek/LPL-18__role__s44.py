class DQNConfiguration:
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
    def __init__(self, configuration: DQNConfiguration):
        self.configuration = configuration
        self.memory = ReplayMemory(capacity=1000)
        self.dqn = DQN(configuration.input_size, configuration.n_actions, configuration.hidden_size, configuration.gamma)
        self.target_dqn = DQN(configuration.input_size, configuration.n_actions, configuration.hidden_size, configuration.gamma)
        self.target_dqn.load_state_dict(self.dqn.state_dict())


def _resumo(agente):
    nomes = ("input_size", "n_actions", "hidden_size", "gamma",
             "batch_size", "epsilon", "epsilon_min", "epsilon_decay")
    return {
        "hiperparametros": {nome: getattr(agente.configuration, nome) for nome in nomes},
        "memoria": (agente.memory.capacity, agente.memory.len()),
        "redes": (agente.dqn.dimensoes, agente.target_dqn.dimensoes),
        "redes_distintas": agente.dqn is not agente.target_dqn,
        "alvo_sincronizado": agente.target_dqn.state_dict()["pesos"] is agente.dqn.state_dict()["pesos"],
    }


def executar(configuracao):
    c = DQNConfiguration(**configuracao)
    agente = DQNAgent(c)
    return _resumo(agente)
