import numpy as np
from scipy.signal import convolve2d


class Game:
    """Estado do jogo: uma matriz 0/1 para cada jogador (X, O) e uma para os bloqueios (B)."""

    def __init__(self, n, s, blocs):
        self.n = n
        self.s = s
        self.blocs = blocs
        self.current_state = {'X': np.zeros((self.n, self.n), dtype=np.int8),
                              'O': np.zeros((self.n, self.n), dtype=np.int8),
                              'B': np.zeros((self.n, self.n), dtype=np.int8)}
        for bloc in self.blocs:
            self.current_state['B'][bloc[0], bloc[1]] = 1
        self.winstates = self._construct_winstates()

    def _construct_winstates(self):
        return (
            np.ones((self.s, 1), dtype=np.int8),  # horizontal
            np.ones((1, self.s), dtype=np.int8),  # vertical
            np.identity(self.s, dtype=np.int8),  # descending
            np.flipud(np.identity(self.s, dtype=bool))  # ascending
        )

    def convolve_winstates(self, state):
        """Convolves each of the possible win states (horizontal, vertical, ascending, descending)
        with the given player's board state and returns a list of the results."""
        return [convolve2d(state, winstate, mode='valid') for winstate in self.winstates]


class Agent:
    def __init__(self, player):
        self.p = player

    def heuristic_1(self, game):
        """heuristic 1: a weighted sum of the number of k-in-a-rows that a player has.
        Calculated by counting the number of potential winstates with (2 to s) pieces in them.
        """

        score = 0

        convs = game.convolve_winstates(game.current_state[self.p])
        for conv in convs:
            if game.s in conv:
                return float('inf')
        convs = game.convolve_winstates(game.current_state['X' if self.p == 'O' else 'O'])
        for conv in convs:
            if game.s in conv:
                return float('-inf')

        for conv in convs:
            score += np.count_nonzero(conv == game.s) << (game.s << 1)
        return score


def executar(linhas, s, jogador):
    """Avalia o tabuleiro para o jogador. Ponto de entrada publico desta unidade.

    linhas: uma string por linha do tabuleiro; 'X' e 'O' sao pecas, '*' e
    bloqueio e qualquer outro caractere e casa vazia.
    """
    blocs = [(x, y) for x, linha in enumerate(linhas) for y, casa in enumerate(linha) if casa == '*']
    game = Game(len(linhas), s, blocs)
    for x, linha in enumerate(linhas):
        for y, casa in enumerate(linha):
            if casa in ('X', 'O'):
                game.current_state[casa][x, y] = 1
    return Agent(jogador).heuristic_1(game)
