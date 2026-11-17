import numpy as np
from scipy.signal import convolve2d

class PlayerState:
    """Game state: one 0/1 matrix per player  (X, O)."""
    def __init__(self, n):
        self.state = np.zeros((n,n), dtype=np.int8)

class BlocState:
    """Game state: one 0/1 matrix for the blocks (B)."""
    def __init__(self, n, blocs):
        self.state = np.zeros((n,n), dtype=np.int8)
        for bloc in blocs:
            self.state[bloc[0],bloc[1]] = 1

class Game:
    """Game state: one 0/1 matrix per player  (X, O) and one for the blocks (B)."""
    def __init__(self, n, s, blocs):
        self.n = n
        self.s = s
        self.player_state = PlayerState(n)
        self.opponent_state = PlayerState(n)
        self.bloc_state = BlocState(n, blocs)
        self.construct_winstates()

    # Rest of the code remains the same
