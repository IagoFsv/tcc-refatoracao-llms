class RedeParams:
    def __init__(self, input_size, n_actions, hidden_size, gamma):
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma

def executar(params: RedeParams):
    rede = DQN(params.input_size, params.n_actions, params.hidden_size, params.gamma)
    return _resumo(rede)
