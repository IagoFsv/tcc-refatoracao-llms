"""Heuristica de avaliacao de um jogo de alinhar pecas num tabuleiro n x n.

Ponto de entrada publico: executar(linhas, s, jogador). Nao altere o nome nem
a assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

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
        self.construct_winstates()

    def construct_winstates(self):
        """Generates a list of all the possible win states (horizontal, vertical, ascending, descending)
        for use determining win condition and in heuristic calculation."""
        self.winstates = [
            np.ones((self.s, 1), dtype=np.int8),  # horizontal
            np.ones((1, self.s), dtype=np.int8),  # vertical
            np.identity(self.s, dtype=np.int8),  # descending
            np.flipud(np.identity(self.s, dtype=bool))  # ascending
        ]

    def convolve_winstates(self, state):
        """Convolves each of the possible win states (horizontal, vertical, ascending, descending)
        with the given player's board state and returns a list of the results.
        Used for determining win conditions, and for heuristic calculation."""
        convs = []
        for winstate in self.winstates:
            convs.append(convolve2d(state, winstate, mode='valid'))
        return convs


class Agent:
    def __init__(self, player):
        self.p = player

    def heuristic_1(self, game):
        """Heuristic 1: a weighted sum of the number of k-in-a-rows that a player has.
        Calculated by counting the number of potential win states with (2 to s) pieces in them.
        """
        score = 0

        # Convolve the individual board states
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

        # Combine the convolved matrices to a usable state
        # Any entry in our convolution that also has an entry in the opponents, or in b, is blocked.
        for i in range(len(convs[0])):
            for j in range(1, game.s):
                # Score: the number of unobstructed win conditions, weighted by 2^(length of the condition)
                # This feels like code golf and GitHub Copilot had a child, and it's ugly
                score += (np.count_nonzero(convs[0][i][convs[1][i] + convs[2][i] == 0] == j) -
                          np.count_nonzero(convs[1][i][convs[0][i] + convs[2][i] == 0] == j)) << (j << 1)
        return score


def executar(linhas, s, jogador):
    """Avalia o tabuleiro para o jogador. Ponto de entrada publico desta unidade.

    linhas: uma string por linha do tabuleiro; 'X' e 'O' são peças, '*' é bloqueio e qualquer outro caractere é casa vazia.
    """
    blocs = [(x, y) for x, linha in enumerate(linhas) for y, casa in enumerate(linha) if casa == '*']
    game = Game(len(linhas), s, blocs)
    for x, linha in enumerate(linhas):
        for y, casa in enumerate(linha):
            if casa in ('X', 'O'):
                game.current_state[casa][x, y] = 1
    return Agent(jogador).heuristic_1(game)
