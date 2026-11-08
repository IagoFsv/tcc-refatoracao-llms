class Dimensoes:
    def __init__(self, input_size, n_actions, hidden_size, gamma):
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma

def executar(dimensoes):
    rede = DQN(dimensoes.input_size, dimensoes.n_actions, dimensoes.hidden_size, dimensoes.gamma)
    return _resumo(rede)
