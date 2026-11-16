class Location:
    """Uma casa do mapa; o terreno so existe depois de gerado."""

    def __init__(self, x, y, z):
        self.location = (x, y, z)
        self.terrain = None

    def generate_terrain(self):
        self.terrain = "grass"


class Fileira:
    """Uma fileira na estrutura do mundo, contendo Location."""

    def __init__(self, tamanho_y, tamanho_z):
        self.fileira = [Location(x, y, z) for z in range(tamanho_z) for y in range(tamanho_y)]

    def generate_terrain(self, x):
        for location in self.fileira:
            location.generate_terrain()


class Plano:
    """Um plano na estrutura do mundo, contendo Fileira."""

    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.plano = [Fileira(tamanho_y, tamanho_z) for x in range(tamanho_x)]

    def generate_terrain(self, x, y):
        self.plano[x].generate_terrain(y)


class World:
    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.world_map_size_x = tamanho_x
        self.world_map_size_y = tamanho_y
        self.world_map_size_z = tamanho_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [Plano(self.world_map_size_x, self.world_map_size_y, self.world_map_size_z) for _ in range(self.world_map_size_z)]


def executar(x, y, z):
    """Gera o terreno na posicao (x, y, z) de um mapa 2 x 3 x 4 e devolve as
    posicoes que tem terreno. Ponto de entrada publico desta unidade."""
    mundo = World(2, 3, 4)
    mundo.world_map[z].plano[y].generate_terrain(x, y)
    return [casa.location for plano in mundo.world_map for fileira in plano.plano for casa in fileira.fileira
            if casa.terrain is not None]
