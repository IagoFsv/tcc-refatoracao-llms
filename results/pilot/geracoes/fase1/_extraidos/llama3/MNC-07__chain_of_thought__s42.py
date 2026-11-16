import numpy as np
from scipy.signal import convolve2d


class Game:
    """Estado do jogo: uma matriz 0/1 para cada jogador (X, O) e uma para os bloqueios (B)."""

    def __init__(self, n, s, blocs):
        self.n = n
        self.s = s
        self.blocs = blocs
        self.x_state = np.zeros((self.n, self.n), dtype=np.int8)
        self.o_state = np.zeros((self.n, self.n), dtype=np.int8)
        self.b_state = np.zeros((self.n, self.n), dtype=np.int8)
        for bloc in self.blocs:
            self.b_state[bloc[0], bloc[1]] = 1
        self.construct_winstates()

    def construct_winstates(self):
        """Gera uma lista de todos os possíveis estados de vitória (horizontal, vertical, ascendente, descendente)
        para uso na determinação do estado de vitória e no cálculo de heurística."""
        self.winstates = (
            np.ones((self.s, 1), dtype=np.int8),  # horizontal
            np.ones((1, self.s), dtype=np.int8),  # vertical
            np.identity(self.s, dtype=np.int8),  # descendente
            np.flipud(np.identity(self.s, dtype=bool))  # ascendente
        )

    def convolve_winstates(self, state):
        """Convolves cada um dos possíveis estados de vitória (horizontal, vertical, ascendente, descendente)
        com o estado do jogador dado e retorna uma lista dos resultados. Usado para determinar o estado de vitória e para cálculo de heurística."""
        convs = []
        for winstate in self.winstates:
            convs.append(convolve2d(state, winstate, mode='valid'))
        return convs


class Agent:
    def __init__(self, player):
        self.p = player

    def heuristic_1(self, game):
        """Heurística 1: uma soma ponderada do número de k-em-linhas que um jogador tem.
        Calculada contando o número de estados de vitória potenciais com (2 a s) peças neles."""
        score = 0

        convs = [game.convolve_winstates(game.x_state), game.convolve_winstates(game.o_state), game.convolve_winstates(game.b_state)]

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


def executar(linhas, s, jogador):
    """Avalia o tabuleiro para o jogador. Ponto de entrada público desta unidade.

    linhas: uma string por linha do tabuleiro; 'X' e 'O' são peças, '*' é bloqueio e qualquer outro caractere é casa vazia."""
    blocs = [(x, y) for x, linha in enumerate(linhas) for y, casa in enumerate(linha) if casa == '*']
    game = Game(len(linhas), s, blocs)
    for x, linha in enumerate(linhas):
        for y, casa in enumerate(linha):
            if casa in ('X', 'O'):
                if casa == 'X':
                    game.x_state[x, y] = 1
                else:
                    game.o_state[x, y] = 1
    return Agent(jogador).heuristic_1(game)
