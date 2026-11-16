class Location:
    """Uma casa do mapa, identificada pelas coordenadas."""

    def __init__(self, x, y, z):
        self.location = (x, y, z)


class World:
    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.world_map_size_x = tamanho_x
        self.world_map_size_y = tamanho_y
        self.world_map_size_z = tamanho_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = []
        for x in range(self.world_map_size_x):
            self.world_map.append(self.generate_layer(x))

    def generate_layer(self, x):
        layer = []
        for y in range(self.world_map_size_y):
            layer.append(self.generate_row(x, y))
        return layer

    def generate_row(self, x, y):
        row = []
        for z in range(self.world_map_size_z):
            row.append(Location(x, y, z))
        return row

    def get_location(self, x, y, z):
        return self.world_map[x][y][z]


def executar(x, y, z):
    """Devolve as coordenadas da casa achada em (x, y, z) num mapa 2 x 3 x 4.
    Ponto de entrada publico desta unidade."""
    return World(2, 3, 4).get_location(x, y, z).location
