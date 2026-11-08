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

    def get_location(self, x, y, z):
        return Location(x, y, z)

    def executar(self, x, y, z):
        """Gera o terreno na posicao (x, y, z) de um mapa 2 x 3 x 4 e devolve as
        posicoes que tem terreno. Ponto de entrada publico desta unidade."""
        location = self.get_location(x, y, z)
        location.generate_terrain()
        return [location.location for location in [location] if location.terrain is not None]
