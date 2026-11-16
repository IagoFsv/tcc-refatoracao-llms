class Location:
    """Uma casa do mapa, identificada pelas coordenadas."""

    def __init__(self, x, y, z):
        self.location = (x, y, z)


class World:
    """Um mapa tridimensional de um jogo de aventura."""

    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.world_map_size_x = tamanho_x
        self.world_map_size_y = tamanho_y
        self.world_map_size_z = tamanho_z
        self.world_map = self.generate_world_map()

    def generate_world_map(self):
        """Gera um mapa 3D para o jogo de aventura."""
        world_map = []
        for x in range(self.world_map_size_x):
            x_world = []
            for y in range(self.world_map_size_y):
                y_world = []
                for z in range(self.world_map_size_z):
                    y_world.append(Location(x, y, z))
                x_world.append(y_world)
            world_map.append(x_world)
        return world_map

    def get_location(self, x, y, z):
        """Devolve uma localização específica no mapa."""
        return self.world_map[x][y][z]


def executar(x, y, z):
    """Devolve as coordenadas da casa achada em uma localização (x, y, z) num mapa 2 x 3 x 4.
    Ponto de entrada publico desta unidade."""
    return World(2, 3, 4).get_location(x, y, z).location
