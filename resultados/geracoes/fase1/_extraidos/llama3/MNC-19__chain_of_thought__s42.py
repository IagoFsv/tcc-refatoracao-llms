class Location:
    """Uma casa do mapa, identificada pelas coordenadas."""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class WorldMap:
    """O mapa do mundo, representado por uma estrutura de dados 2D."""

    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.size_x = tamanho_x
        self.size_y = tamanho_y
        self.size_z = tamanho_z
        self.locations = [[[] for _ in range(tamanho_y)] for _ in range(tamanho_x)]

    def generate_world_map(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                for z in range(self.size_z):
                    self.locations[x][y].append(Location(x, y, z))

    def get_location(self, x, y, z):
        return self.locations[x][y][z]


def executar(x, y, z):
    """Devolve as coordenadas da casa achada em (x, y, z) num mapa 2 x 3 x 4.
    Ponto de entrada publico desta unidade."""
    world_map = WorldMap(2, 3, 4)
    world_map.generate_world_map()
    return world_map.get_location(x, y, z).location
