class GameState:
    def __init__(self, n, s, blocs):
        self.n = n
        self.s = s
        self.blocs = blocs
        self.board = {'X': np.zeros((n, n), dtype=np.int8),
                      'O': np.zeros((n, n), dtype=np.int8),
                      'B': np.zeros((n, n), dtype=np.int8)}
        for bloc in self.blocs:
            self.board['B'][bloc[0], bloc[1]] = 1

    def convolve_winstates(self, state):
        convs = []
        for winstate in self.winstates:
            convs.append(convolve2d(state, winstate, mode='valid'))
        return convs

class WinState:
    def __init__(self, s):
        self.s = s
        self.states = (np.ones((s, 1), dtype=np.int8),  # horizontal
                       np.ones((1, s), dtype=np.int8),  # vertical
                       np.identity(s, dtype=np.int8),  # descending
                       np.flipud(np.identity(s, dtype=bool)))  # ascending

class Agent:
    def __init__(self, player):
        self.p = player

    def heuristic_1(self, game_state):
        score = 0

        convs = [game_state.convolve_winstates(game_state.board[self.p]),
                 game_state.convolve_winstates(game_state.board['X' if self.p == 'O' else 'O']),
                 game_state.convolve_winstates(game_state.board['B'])]

        for conv in convs[0]:
            if game_state.s in conv:
                return float('inf')
        for conv in convs[1]:
            if game_state.s in conv:
                return float('-inf')

        for i in range(len(convs[0])):
            for j in range(1, game_state.s):
                score += (np.count_nonzero(convs[0][i][convs[1][i] + convs[2][i] == 0] == j) -
                          np.count_nonzero(convs[1][i][convs[0][i] + convs[2][i] == 0] == j)) << (j << 1)
        return score

def executar(linhas, s, jogador):
    blocs = [(x, y) for x, linha in enumerate(linhas) for y, casa in enumerate(linha) if casa == '*']
    game_state = GameState(len(linhas), s, blocs)
    for x, linha in enumerate(linhas):
        for y, casa in enumerate(linha):
            if casa in ('X', 'O'):
                game_state.board[casa][x, y] = 1
    return Agent(jogador).heuristic_1(game_state)
