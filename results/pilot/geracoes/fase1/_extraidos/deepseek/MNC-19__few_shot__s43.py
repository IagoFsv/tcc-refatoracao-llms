from dataclasses import dataclass

@dataclass
class Location:
    """Uma casa do mapa, identificada pelas coordenadas."""
    x: int
    y: int
    z: int


class World:
    """Um mapa tridimensional."""
    def __init__(self, tamanho_x: int, tamanho_y: int, tamanho_z: int):
        self.world_map_size_x = tamanho_x
        self.world_map_size_y = tamanho_y
        self.world_map_size_z = tamanho_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [[[Location(x, y, z) for z in range(self.world_map_size_z)] for y in range(self.world_map_size_y)] for x in range(self.world_map_size_x)]

    def get_location(self, x: int, y: int, z: int) -> Location:
        return self.world_map[x][y][z]


def executar(x: int, y: int, z: int) -> Location:
    """Devolve as coordenadas da casa achada em uma posição (x, y, z) num mapa 2x3x4.
    Ponto de entrada público desta unidade."""
    return World(2, 3, 4).get_location(x, y, z)
