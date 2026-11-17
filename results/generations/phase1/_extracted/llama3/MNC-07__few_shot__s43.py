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
        self.winstates = (
            np.ones((self.s, 1), dtype=np.int8),  # horizontal
            np.ones((1, self.s), dtype=np.int8),  # vertical
            np.identity(self.s, dtype=np.int8),  # descending
            np.flipud(np.identity(self.s, dtype=bool))  # ascending
        )

    def convolve_winstates(self, state):
        convs = []
        for winstate in self.winstates:
            convs.append(convolve2d(state, winstate, mode='valid'))
        return convs

class Board:
    def __init__(self, n, s):
        self.n = n
        self.s = s
        self.state = np.zeros((n, n), dtype=np.int8)

    def set_piece(self, x, y, piece):
        self.state[x, y] = 1 if piece == 'X' else 2

    def get_piece(self, x, y):
        return 0 if self.state[x, y] == 0 else (1 if self.state[x, y] == 1 else 2)

    def convolve(self, winstate):
        return convolve2d(self.state, winstate, mode='valid')

class Agent:
    def __init__(self, player):
        self.p = player

    def heuristic_1(self, game):
        score = 0

        convs = []
        for piece in ['X', 'O', 'B']:
            convs.append(game.convolve_winstates(game.current_state[piece]))

        for conv in convs[0]:
            if game.s in conv:
                return float('inf')
        for conv in convs[1]:
            if game.s in conv:
                return float('-inf')

        for i in range(len(convs[0])):
            for j in range(1, game.s):
                score += (np.count_nonzero(convs[0][i][convs[1][i] + convs[2][i] == 0] == j) - np.count_nonzero(convs[1][i][convs[0][i] + convs[2][i] == 0] == j)) << (j << 1)
        return score

def run(rows, s, player):
    blocs = [(x, y) for x, row in enumerate(rows) for y, cell in enumerate(row) if cell == '*']
    game = Game(len(rows), s, blocs)
    board = Board(len(rows), s)
    for x, row in enumerate(rows):
        for y, cell in enumerate(row):
            if cell in ('X', 'O'):
                board.set_piece(x, y, cell)
    game.current_state = {'X': board.state.copy(), 'O': board.state.copy(), 'B': board.state.copy()}
    return Agent(player).heuristic_1(game)
