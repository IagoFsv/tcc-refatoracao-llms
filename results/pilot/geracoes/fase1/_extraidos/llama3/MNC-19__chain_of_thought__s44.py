class Location:
    """Uma casa do mapa, identificada pelas coordenadas."""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class LocationMap:
    """O mapa do mundo, representado por uma matriz de Location."""

    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.size_x = tamanho_x
        self.size_y = tamanho_y
        self.size_z = tamanho_z
        self.locations = self.generate_world_map()

    def generate_world_map(self):
        return [[Location(x, y, z) for z in range(self.size_z)] for y in range(self.size_y)] for x in range(self.size_x)]

    def get_location(self, x, y, z):
        return self.locations[x][y][z]

def executar(x, y, z):
    """Devolve as coordenadas da casa achada em (x, y, z) num mapa 2 x 3 x 4.
    Ponto de entrada publico desta unidade."""
    world_map = LocationMap(2, 3, 4)
    return world_map.get_location(x, y, z).x, world_map.get_location(x, y, z).y, world_map.get_location(x, y, z).z
