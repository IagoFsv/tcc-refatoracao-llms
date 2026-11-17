"""Evaluation heuristic of a game of lining up pieces on an n x n board.

Public entry point: run(rows, s, player). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import numpy as np
from scipy.signal import convolve2d

class Board:
    def __init__(self, n, s, blocs):
        self.n = n
        self.s = s
        self.blocs = blocs
        self.state = np.zeros((self.n, self.n), dtype=np.int8)
        self.set_blocks()
        self.construct_winstates()

    def set_blocks(self):
        for bloc in self.blocs:
            self.state[bloc[0], bloc[1]] = 1

    def construct_winstates(self):
        self.winstates = (
            np.ones((self.s, 1), dtype=np.int8),
            np.ones((1, self.s), dtype=np.int8),
            np.identity(self.s, dtype=np.int8),
            np.flipud(np.identity(self.s, dtype=bool))
        )

    def convolve_winstates(self, state):
        convs = []
        for winstate in self.winstates:
            convs.append(convolve2d(state, winstate, mode='valid'))
        return convs

class Player:
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

        for i in range(len(convs[0])):
            for j in range(1, game.s):
                score += (np.count_nonzero(convs[0][i][convs[1][i] + convs[2][i] == 0] == j) - 
                          np.count_nonzero(convs[1][i][convs[0][i] + convs[2][i] == 0] == j)) << (j << 1)
        return score

class Game:
    def __init__(self, board, player):
        self.board = board
        self.player = player

    def run(self):
        return Player(self.player).heuristic_1(self)

def run(rows, s, player):
    blocs = [(x, y) for x, row in enumerate(rows) for y, cell in enumerate(row) if cell == '*']
    board = Board(len(rows), s, blocs)
    for x, row in enumerate(rows):
        for y, cell in enumerate(row):
            if cell in ('X', 'O'):
                board.state[x, y] = 1
    game = Game(board, player)
    return game.run()
