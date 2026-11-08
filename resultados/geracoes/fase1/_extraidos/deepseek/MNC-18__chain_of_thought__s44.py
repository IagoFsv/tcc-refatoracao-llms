class World:
    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.world_map_size_x = tamanho_x
        self.world_map_size_y = tamanho_y
        self.world_map_size_z = tamanho_z
        self.world_map = self.generate_world_map()

    def generate_world_map(self):
        return [[[None for _ in range(self.world_map_size_z)] for _ in range(self.world_map_size_y)] for _ in range(self.world_map_size_x)]

    def generate_terrain(self, x, y, z):
        if self.world_map[x][y][z] is None:
            self.world_map[x][y][z] = "grass"


def executar(x, y, z):
    """Gera o terreno na posicao  (x, y, z) de um mapa 2 x 3 x 4 e devolve as
    posicoes que tem terreno. Ponto de entrada publico desta unidade."""
    mundo = World(2, 3, 4)
    mundo.generate_terrain(x, y, z)
    return [(x, y, z) for x in range(mundo.world_map_size_x) for y in range(mundo.world_map_size_y) for z in range(mundo.world_map_size_z) if mundo.world_map[x][y][z] is not None]
