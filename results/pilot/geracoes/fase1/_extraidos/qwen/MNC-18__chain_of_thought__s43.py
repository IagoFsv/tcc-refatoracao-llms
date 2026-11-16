class Location:
    """Uma casa do mapa; o terreno so existe depois de gerado."""

    def __init__(self, x, y, z):
        self.location = (x, y, z)
        self.terrain = None

    def generate_terrain(self):
        self.terrain = "grass"


class Plane:
    def __init__(self, tamanho_y, tamanho_z):
        self.plane = [[Location(x, y, z) for z in range(tamanho_z)] for y in range(tamanho_y)]

    def generate_terrain(self, x):
        for y in range(len(self.plane)):
            for z in range(len(self.plane[y])):
                self.plane[y][z].generate_terrain()


class Row:
    def __init__(self, tamanho_z):
        self.row = [Location(x, y, z) for z in range(tamanho_z)]

    def generate_terrain(self, x, y):
        for z in range(len(self.row)):
            self.row[z].generate_terrain()


class World:
    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.world_map_size_x = tamanho_x
        self.world_map_size_y = tamanho_y
        self.world_map_size_z = tamanho_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [Plane(self.world_map_size_y, self.world_map_size_z) for _ in range(self.world_map_size_x)]
        for x in range(self.world_map_size_x):
            for y in range(self.world_map_size_y):
                self.world_map[x].plane[y].generate_terrain(x)


def generate_terrain(self, x, y, z):
    self.world_map[x].plane[y].row[z].generate_terrain(x, y)


def executar(x, y, z):
    """Gera o terreno na posicao (x, y, z) de um mapa 2 x 3 x 4 e devolve as posicoes que tem terreno. Ponto de entrada publico desta unidade."""
    mundo = World(2, 3, 4)
    mundo.generate_terrain(x, y, z)
    return [casa.location for plano in mundo.world_map for fileira in plano.plane for casa in fileira.row if casa.terrain is not None]
