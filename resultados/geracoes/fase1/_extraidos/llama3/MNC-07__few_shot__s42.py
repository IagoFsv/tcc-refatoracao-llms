import numpy as np
from scipy.signal import convolve2d

class Game:
    def __init__(self, n, s, blocs):
        self.n = n
        self.s = s
        self.blocs = blocs
        self.current_state = {'X': np.zeros((self.n, self.n), dtype=np.int8),
                              'O': np.zeros((self.n, self.n), dtype=np.int8),
                              'B': np.zeros((self.n, self.n), dtype=np.int8)}
        for bloc in self.blocs:
            self.current_state['B'][bloc[0], bloc[1]] = 1
        self.construct_winstates()

    def construct_winstates(self):
        self.winstates = {'horizontal': np.ones((self.s, 1), dtype=np.int8),
                         'vertical': np.ones((1, self.s), dtype=np.int8),
                         'ascending': np.identity(self.s, dtype=np.int8),
                         'descending': np.flipud(np.identity(self.s, dtype=bool))}

    def convolve_winstates(self, state):
        convs = []
        for winstate in self.winstates.values():
            convs.append(convolve2d(state, winstate, mode='valid'))
        return convs

    def get_winstates(self):
        return self.winstates

class Agent:
    def __init__(self, player):
        self.p = player

    def heuristic_1(self, game):
        score = 0
        convs = [game.convolve_winstates(game.current_state[self.p]),
                 game.convolve_winstates(game.current_state['X' if self.p == 'O' else 'O']),
                 game.convolve_winstates(game.current_state['B'])]

        for conv in convs[0]:
            if game.s in conv:
                return float('inf')
        for conv in convs[1]:
            if game.s in conv:
                return float('-inf')

        for conv in convs[0]:
            if conv.any():
                score += np.count_nonzero(conv)

        return score

def executar(linhas, s, jogador):
    blocs = [(x, y) for x, linha in enumerate(linhas) for y, casa in enumerate(linha) if casa == '*']
    game = Game(len(linhas), s, blocs)
    for x, linha in enumerate(linhas):
        for y, casa in enumerate(linha):
            if casa in ('X', 'O'):
                game.current_state[casa][x, y] = 1
    return Agent(jogador).heuristic_1(game)
