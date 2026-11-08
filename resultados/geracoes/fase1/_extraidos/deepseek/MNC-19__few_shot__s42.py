"""Mapa tridimensional de um jogo de aventura: consulta de uma posicao.

Ponto de entrada publico: executar(x, y, z). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""


class Location:
    """Uma casa do mapa, identificada pelas coordenadas."""

    def __init__(self, x, y, z):
        self.coordenadas = (x, y, z)


class World:
    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.tamanho_x = tamanho_x
        self.tamanho_y = tamanho_y
        self.tamanho_z = tamanho_z
        self.gerar_mapa_mundo()

    def gerar_mapa_mundo(self):
        self.mapa_mundo = [[[Location(x, y, z) for z in range(self.tamanho_z)] for y in range(self.tamanho_y)] for x in range(self.tamanho_x)]

    def obter_localizacao(self, x, y, z):
        return self.mapa_mundo[x][y][z]


def executar(x, y, z):
    """Devolve as coordenadas da casa achada em uma posicao (x, y, z) em um mapa 2x3x4.
    Ponto de entrada publico desta unidade."""
    return World(2, 3, 4).obter_localizacao(x, y, z).coordenadas
