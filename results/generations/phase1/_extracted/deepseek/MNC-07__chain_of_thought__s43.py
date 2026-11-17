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
        self.current_state_X = np.zeros((self.n,self.n), dtype=np.int8)
        self.current_state_O = np.zeros((self.n,self.n), dtype=np.int8)
        self.current_state_B = np.zeros((self.n,self.n), dtype=np.int8)
        for bloc in self.blocs:
            self.current_state_B[bloc[0],bloc[1]] = 1
        self.construct_winstates()

    # ... rest of the code remains the same ...

class Agent:
    def __init__(self, player):
        self.p = player

    # ... rest of the code remains the same ...

def run(rows, s, player):
    """Evaluates the board for the player. Public entry point of this unit.

    rows: one string per board row; 'X' and 'O' are pieces, 
    '*' is a block and any other character is an empty cell.
    """
    blocs = [(x, y) for x, row in enumerate(rows) for y, cell in enumerate(row) if cell == '*']
    game = Game(len(rows), s, blocs)
    for x, row in enumerate(rows):
        for y, cell in enumerate(row):
            if cell in ('X', 'O'):
                game.current_state_X[x, y] = 1 if cell == 'X' else 0
                game.current_state_O[x, y] = 1 if cell == 'O' else 0
    return Agent(player).heuristic_1(game)
