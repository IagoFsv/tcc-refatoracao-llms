class Location:
    """Uma casa do mapa, identificada pelas coordenadas."""

    def __init__(self, x, y, z):
        self.location = (x, y, z)


class Row:
    """Uma linha dentro de uma camada do mapa."""

    def __init__(self, y, z, size_x):
        self.locations = [Location(x, y, z) for x in range(size_x)]

    def get_location(self, x):
        return self.locations[x]


class Layer:
    """Uma camada do mapa (z-axis)."""

    def __init__(self, z, size_x, size_y):
        self.rows = [Row(y, z, size_x) for y in range(size_y)]

    def get_location(self, x, y):
        return self.rows[y].get_location(x)


class World:
    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.world_map_size_x = tamanho_x
        self.world_map_size_y = tamanho_y
        self.world_map_size_z = tamanho_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [Layer(z, self.world_map_size_x, self.world_map_size_y) for z in range(self.world_map_size_z)]

    def get_location(self, x, y, z):
        return self.world_map[z].get_location(x, y)


def executar(x, y, z):
    """Devolve as coordenadas da casa achada em (x, y, z) num mapa 2 x 3 x 4.
    Ponto de entrada publico desta unidade."""
    return World(2, 3, 4).get_location(x, y, z).location
