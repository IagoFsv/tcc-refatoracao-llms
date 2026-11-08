class Location:
    """Uma casa do mapa; o terreno so existe depois de gerado."""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.terrain = None

    def generate_terrain(self):
        self.terrain = "grass"


class World:
    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.world_map_size_x = tamanho_x
        self.world_map_size_y = tamanho_y
        self.world_map_size_z = tamanho_z

    def generate_world_map(self):
        self.world_map = []
        for x in range(self.world_map_size_x):
            self.world_map.append([])
            for y in range(self.world_map_size_y):
                self.world_map[x].append([])
                for z in range(self.world_map_size_z):
                    self.world_map[x][y].append(Location(x, y, z))

    def generate_terrain(self, x, y, z):
        self.world_map[x][y][z].generate_terrain()


def executar(x, y, z):
    """Gera o terreno na posicao (x, y, z) de um mapa 2 x 3 x 4 e devolve as
    posicoes que tem terreno. Ponto de entrada publico desta unidade."""
    mundo = World(2, 3, 4)
    mundo.generate_world_map()
    mundo.generate_terrain(x, y, z)
    return [casa.location for fileira in mundo.world_map[x] for casa in fileira if casa.terrain is not None]
