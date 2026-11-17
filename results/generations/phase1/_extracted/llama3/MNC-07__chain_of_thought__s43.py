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
        for bloc in self.blocs:
            self.current_state['B'][bloc[0], bloc[1]] = 1
        self.construct_winstates()

    def construct_winstates(self):
        '''generates a list of all the possible winstates (horizontal, vertical, ascending, descending)
        for use determining win condition and in heuristic calculation.'''
        self.winstates = (
            np.ones((self.s, 1), dtype=np.int8),  # horizontal
            np.ones((1, self.s), dtype=np.int8),  # vertical
            np.identity(self.s, dtype=np.int8),  # descending
            np.flipud(np.identity(self.s, dtype=bool))  # ascending
        )

    def convolve_winstates(self, state):
        '''Convolves each of the possible win states (horizontal, vertical, ascending, descending)
        with the given player's board state and returns a list of the results. Used for determining win conditions, and for heuristic calculation.'''
        convs = []
        # perform the convolution on every winstate
        for winstate in self.winstates:
            convs.append(convolve2d(state, winstate, mode='valid'))
        return convs

    def get_player_state(self, player):
        return self.current_state[player]

    def get_opponent_state(self, player):
        return self.current_state['X' if player == 'O' else 'O']

    def get_block_state(self):
        return self.current_state['B']

    def has_won(self, player):
        for conv in self.convolve_winstates(self.get_player_state(player)):
            if self.s in conv:
                return True
        return False

    def count_unobstructed_winstates(self, conv):
        score = 0
        for i in range(len(conv)):
            for j in range(1, self.s):
                if conv[i][j] == 0:
                    score += (np.count_nonzero(conv[i][j] == j) - np.count_nonzero(conv[i][j] == j)) << (j << 1)
        return score


class Agent:
    def __init__(self, player):
        self.p = player

    def heuristic_1(self, game):
        '''heuristic 1: a weighted sum of the number of k-in-a-rows that a player has.
        Calculated by counting the number of potential winstates with (2 to s) pieces in them.
        '''

        score = 0

        # convolve the individual board states
        convs = [game.convolve_winstates(game.get_player_state(self.p)),
                 game.convolve_winstates(game.get_opponent_state(self.p)),
                 game.convolve_winstates(game.get_block_state())]

        # set score to +/- inf if one player has won
        if game.has_won(self.p):
            return float('inf')
        if game.has_won('O' if self.p == 'X' else 'X'):
            return float('-inf')

        # combines the convolved matricies to a usable state
        # any entry in our convolution that also has an entry in the opponents, or in b, is blocked.
        for conv in convs[0]:
            if conv[0] == 1:
                score += game.count_unobstructed_winstates(conv)
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
