"""Evaluation heuristic of a game of lining up pieces on an n x n board.

Public entry point: run(rows, s, player). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import numpy as np
from scipy.signal import convolve2d

class Game:
    """Game state: one 0/1 matrix per player (X, O) and one for the blocks (B)."""

    def __init__(self, n, s, blocs):
        self.n = n
        self.s = s
        self.blocs = blocs
        self.current_state = {'X': np.zeros((self.n,self.n), dtype=np.int8),
                              'O':np.zeros((self.n,self.n), dtype=np.int8),
                              'B':np.zeros((self.n,self.n), dtype=np.int8)}
        for bloc in self.blocs:
            self.current_state['B'][bloc[0],bloc[1]] = 1
        self.winstates = self._construct_winstates()
        self.agent = Agent()

    def _construct_winstates(self):
        return (
            np.ones((self.s,1), dtype=np.int8),    #horizontal
            np.ones((1,self.s), dtype=np.int8),    #vertical
            np.identity(self.s, dtype=np.int8),    #descending
            np.flipud(np.identity(self.s, dtype=bool))  #ascending
        )

    def convolve_winstates(self, state):
        return [convolve2d(state, winstate, mode='valid') for winstate in self.winstates]

    def construct_agent(self):
        self.agent = Agent(self.p)

    def heuristic_1(self, game):
        score = 0

        convs = self.convolve_winstates(game.current_state[self.p])
        for conv in convs:
            if self.s in conv:
                return float('inf')
        convs = self.convolve_winstates(game.current_state['X' if self.p == 'O' else 'O'])
        for conv in convs:
            if self.s in conv:
                return float('-inf')

        for i in range(len(convs[0])):
            for j in range(1,self.s):
                score += (np.count_nonzero(convs[0][i][convs[1][i]+convs[2][i] == 0] == j) - np.count_nonzero(convs[1][i][convs[0][i]+convs[2][i] == 0] == j))<<(j<<1)
        return score

class Agent:
    def __init__(self, player):
        self.p = player

    def evaluate(self, game):
        return game.heuristic_1(game)

def run(rows, s, player):
    """Evaluates the board for the player. Public entry point of this unit.

    rows: one string per board row; 'X' and 'O' are pieces, '*' is a block
    and any other character is an empty cell.
    """
    blocs = [(x, y) for x, row in enumerate(rows) for y, cell in enumerate(row) if cell == '*']
    game = Game(len(rows), s, blocs)
    for x, row in enumerate(rows):
        for y, cell in enumerate(row):
            if cell in ('X', 'O'):
                game.current_state[cell][x, y] = 1
    game.construct_agent()
    return game.agent.evaluate(game)
