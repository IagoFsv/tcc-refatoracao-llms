class Location:
    """Uma casa do mapa, identificada pelas coordenadas."""

    def __init__(self, x, y, z):
        self.location = (x, y, z)


class Layer:
    """Um nível do mapa tridimensional."""

    def __init__(self, tamanho_x, tamanho_y):
        self.layer = [[Location(x, y, z) for z in range(tamanho_x)] for y in range(tamanho_y)]

    def get_location(self, x, y):
        return self.layer[x][y]


class World:
    """O mapa tridimensional do jogo de aventura."""

    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.world_map = [Layer(tamanho_x, tamanho_y) for _ in range(tamanho_z)]

    def get_location(self, x, y, z):
        return self.world_map[z].get_location(x, y)


def executar(x, y, z):
    """Devolve as coordenadas da casa achada em uma casa (x, y, z) num mapa 2 x 3 x 4.
    Ponto de entrada publico desta unidade."""
    return World(2, 3, 4).get_location(x, y, z).location
