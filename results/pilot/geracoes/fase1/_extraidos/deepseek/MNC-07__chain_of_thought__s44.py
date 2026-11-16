class GameState:
    """Estado do jogo: uma matriz 0/1 para cada jogador  (X, O) e uma para os bloqueios  (B)."""

    def __init__(self, n, s, blocs):
        self.n = n
        self.s = s
        self.blocs = blocs
        self.current_state = {'X': np.zeros((self.n,self.n), dtype=np.int8),
                               'O':np.zeros((self.n,self.n), dtype=np.int8),
                               'B':np.zeros((self.n,self.n), dtype=np.int8)}
        for bloc in self.blocs:
            self.current_state['B'][bloc[0],bloc[1]] = 1

class WinState:
    """Gera os estados de vitória possíveis para o jogo."""

    def __init__(self, s):
        self.s = s
        self.winstates = self.construct_winstates()

    def construct_winstates(self):
        """gera uma lista de todos os estados de vitória possíveis (horizontal, vertical, ascending, descending)"""
        # implementação aqui

    def convolve_winstates(self, state):
        """Convolve cada um dos estados de vitória possíveis com o estado do tabuleiro dado e retorna uma lista dos resultados. Usado para determinar as condições de vitória e para a heurística de avaliação."""
        # implementação aqui

class Agent:
    # classe original

def executar(linhas, s, jogador):
    # código original
