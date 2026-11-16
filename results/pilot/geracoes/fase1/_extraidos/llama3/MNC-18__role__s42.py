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
        self.tamanho_x = tamanho_x
        self.tamanho_y = tamanho_y
        self.tamanho_z = tamanho_z
        self.world_map = self.generate_world_map()

    def generate_world_map(self):
        return [[[Location(x, y, z) for z in range(self.tamanho_z)] for y in range(self.tamanho_y)] for x in range(self.tamanho_x)]

    def executar(self, x, y, z):
        """Gera o terreno na posicao (x, y, z) de um mapa 2 x 3 x 4 e devolve as
        posicoes que tem terreno. Ponto de entrada publico desta unidade."""
        self.world_map[x][y][z].generate_terrain()
        return [casa.location for casa in self.world_map[x][y] if casa.terrain is not None]
