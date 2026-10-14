"""Agente de aprendizado por reforco com memoria de experiencias.

Ponto de entrada publico: executar(configuracao). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.

A rede Q e uma versao minima: guarda as dimensoes recebidas e um conjunto
de pesos proprio, que pode ser copiado de outra rede; recusa tamanho
negativo, como a versao real.
"""

import random


class DQN:
    """Rede minima: dimensoes recebidas e pesos copiaveis."""

    def __init__(self, *dimensoes):
        input_size, n_actions, hidden_size, gamma = dimensoes
        if min(input_size, n_actions, hidden_size) < 0:
            raise RuntimeError("Trying to create tensor with negative dimension")
        self.dimensoes = dimensoes
        self.pesos = {"pesos": object()}

    def state_dict(self):
        return dict(self.pesos)

    def load_state_dict(self, state_dict):
        self.pesos = dict(state_dict)


class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, *args):
        self.memory.append(args)
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        # debug
        return zip(*random.sample(self.memory, batch_size))
    
    def len(self):
        return len(self.memory)


class DQNAgent:
    def __init__(self, input_size, n_actions, hidden_size, gamma, batch_size, epsilon, epsilon_min, epsilon_decay):
        # define the hyperparameters
        self.input_size = input_size
        self.n_actions = n_actions
        self.hidden_size = hidden_size
        self.gamma = gamma
        self.batch_size = batch_size
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        # create the replay memory
        self.memory = ReplayMemory(capacity=1000)
        # create the DQN
        self.dqn = DQN(input_size, n_actions, hidden_size, gamma)
        # create the target DQN
        self.target_dqn = DQN(input_size, n_actions, hidden_size, gamma)
        # initialize the target DQN
        self.target_dqn.load_state_dict(self.dqn.state_dict())


def _resumo(agente):
    """Hiperparametros guardados, memoria, as duas redes e a sincronia entre elas."""
    nomes = ("input_size", "n_actions", "hidden_size", "gamma",
             "batch_size", "epsilon", "epsilon_min", "epsilon_decay")
    return {
        "hiperparametros": {nome: getattr(agente, nome) for nome in nomes},
        "memoria": (agente.memory.capacity, agente.memory.len()),
        "redes": (agente.dqn.dimensoes, agente.target_dqn.dimensoes),
        "redes_distintas": agente.dqn is not agente.target_dqn,
        "alvo_sincronizado": agente.target_dqn.state_dict()["pesos"] is agente.dqn.state_dict()["pesos"],
    }


def executar(configuracao):
    """configuracao: input_size, n_actions, hidden_size, gamma, batch_size,
    epsilon, epsilon_min e epsilon_decay."""
    c = configuracao
    agente = DQNAgent(c["input_size"], c["n_actions"], c["hidden_size"], c["gamma"],
                      c["batch_size"], c["epsilon"], c["epsilon_min"], c["epsilon_decay"])
    return _resumo(agente)
