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
        '''Gera uma lista de todos os possíveis estados de vitória (horizontal, vertical, ascendente, descendente)'''
        self.winstates = (
            np.ones((self.s, 1), dtype=np.int8),    #horizontal
            np.ones((1, self.s), dtype=np.int8),    #vertical
            np.identity(self.s, dtype=np.int8),    #descendente
            np.flipud(np.identity(self.s, dtype=bool)))  #ascendente

    def convolve_winstates(self, state):
        '''Convolves cada estado de vitória com o tabuleiro do jogador e retorna uma lista dos resultados.'''
        convs = []
        for winstate in self.winstates:
            convs.append(convolve2d(state, winstate, mode='valid'))
        return convs

class Agent:
    def __init__(self, player):
        self.p = player

    def heuristic_1(self, game):
        '''Heurística 1: uma soma ponderada do número de k-in-a-rows que um jogador tem.
        Calculada contando o número de potenciais estados de vitória com (2 a s) peças.
        '''
        score = 0

        # Convolução das estados de vitória do jogador atual e dos oponentes
        convs = self.get_convolutions(game)

        # Verifica se alguém já ganhou
        if self.check_win_conditions(convs[0]):
            return float('inf')
        if self.check_win_conditions(convs[1]):
            return float('-inf')

        # Combina as matrizes convolucionadas para um estado util
        for i in range(len(convs[0])):
            for j in range(1, game.s):
                score += (np.count_nonzero(convs[0][i][convs[1][i] + convs[2][i] == 0] == j) -
                          np.count_nonzero(convs[1][i][convs[0][i] + convs[2][i] == 0] == j)) << (j << 1)

        return score

    def get_convolutions(self, game):
        '''Obtém as convoluções dos estados de vitória'''
        return [
            game.convolve_winstates(game.current_state[self.p]),
            game.convolve_winstates(game.current_state['X' if self.p == 'O' else 'O']),
            game.convolve_winstates(game.current_state['B'])
        ]

    def check_win_conditions(self, convs):
        '''Verifica as condições de vitória'''
        for conv in convs[0]:
            if game.s in conv:
                return True
        for conv in convs[1]:
            if game.s in conv:
                return True
        return False

def executar(linhas, s, jogador):
    """Avalia o tabuleiro para o jogador. Ponto de entrada público desta unidade.

    linhas: uma string por linha do tabuleiro; 'X' e 'O' são pecas, '*' e
    bloqueio e qualquer outro caractere é casa vazia.
    """
    blocs = [(x, y) for x, linha in enumerate(linhas) for y, casa in enumerate(linha) if casa == '*']
    game = Game(len(linhas), s, blocs)
    for x, linha in enumerate(linhas):
        for y, casa in enumerate(linha):
            if casa in ('X', 'O'):
                game.current_state[casa][x, y] = 1
    return Agent(jogador).heuristic_1(game)
