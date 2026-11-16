class Location:
    """Uma casa do mapa; o terreno só existe depois de gerado."""

    def __init__(self, x, y, z):
        self.location = (x, y, z)
        self.terrain = None

    def generate_terrain(self):
        self.terrain = "grass"


class WorldMap:
    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.size_x = tamanho_x
        self.size_y = tamanho_y
        self.size_z = tamanho_z
        self.map = []

    def generate_map(self):
        self.map = [[Location(x, y, z) for z in range(self.size_z)] for y in range(self.size_y)] for x in range(self.size_x)]


class World:
    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.world_map = WorldMap(tamanho_x, tamanho_y, tamanho_z)

    def generate_world_map(self):
        self.world_map.generate_map()

    def generate_terrain(self, x, y, z):
        self.world_map.map[x][y][z].generate_terrain()


def executar(x, y, z):
    """Gera o terreno na posição (x, y, z) de um mapa 2 x 3 x 4 e devolve as
    posições que têm terreno. Ponto de entrada público desta unidade."""
    mundo = World(2, 3, 4)
    mundo.world_map.generate_world_map()
    mundo.world_map.generate_terrain(x, y, z)
    return [casa.location for fileira in mundo.world_map.map for casa in fileira
            if casa.terrain is not None]
