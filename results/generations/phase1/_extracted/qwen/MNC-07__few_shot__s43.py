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
        self.current_state = {'X': np.zeros((self.n, self.n), dtype=np.int8),
                              'O': np.zeros((self.n, self.n), dtype=np.int8),
                              'B': np.zeros((self.n, self.n), dtype=np.int8)}
        self.initialize_blocks()
        self.construct_winstates()

    def initialize_blocks(self):
        for bloc in self.blocs:
            self.current_state['B'][bloc[0], bloc[1]] = 1

    def construct_winstates(self):
        '''Generates a list of all the possible winstates (horizontal, vertical, ascending, descending)
        for use determining win condition and in heuristic calculation.'''
        self.winstates = (
            np.ones((self.s, 1), dtype=np.int8),    # horizontal
            np.ones((1, self.s), dtype=np.int8),    # vertical
            np.identity(self.s, dtype=np.int8),    # descending
            np.flipud(np.identity(self.s, dtype=bool))  # ascending
        )

    def convolve_winstates(self, state):
        '''Convolves each of the possible win states (horizontal, vertical, ascending, descending)
        with the given player's board state and returns a list of the results. Used for determining win conditions, and for heuristic calculation.'''
        convs = []
        for winstate in self.winstates:
            convs.append(convolve2d(state, winstate, mode='valid'))
        return convs


class Agent:
    def __init__(self, player):
        self.p = player

    def heuristic_1(self, game):
        '''Heuristic 1: a weighted sum of the number of k-in-a-rows that a player has.
        Calculated by counting the number of potential winstates with (2 to s) pieces in them.
        '''

        score = 0

        # Convolves the individual board states
        convs = [game.convolve_winstates(game.current_state[self.p]),
                 game.convolve_winstates(game.current_state['X' if self.p == 'O' else 'O']),
                 game.convolve_winstates(game.current_state['B'])]

        # Set score to +/- inf if one player has won
        for conv in convs[0]:
            if game.s in conv:
                return float('inf')
        for conv in convs[1]:
            if game.s in conv:
                return float('-inf')

        # Combines the convolved matrices to a usable state
        for i in range(len(convs[0])):
            for j in range(1, game.s):
                # Score: the number of unobstructed win conditions, weighted by 2^(length of the condition)
                score += (np.count_nonzero(convs[0][i][convs[1][i] + convs[2][i] == 0] == j) -
                          np.count_nonzero(convs[1][i][convs[0][i] + convs[2][i] == 0] == j)) << (j << 1)
        return score


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
    return Agent(player).heuristic_1(game)
