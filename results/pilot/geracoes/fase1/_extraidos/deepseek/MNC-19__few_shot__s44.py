from dataclasses import dataclass

@dataclass
class Location:
    """Uma casa do mapa, identificada pelas coordenadas."""
    x: int
    y: int
    z: int

@dataclass
class World:
    """Um mapa 3D de um jogo de aventura."""
    tamanho_x: int
    tamanho_y: int
    tamanho_z: int
    
    def generate_world_map(self):
        self.world_map = [[[Location(x, y, z) for z in range(self.tamanho_z)] for y in range(self.tamanho_y)] for x in range(self.tamanho_x)]

    def get_location(self, x, y, z):
        return self.world_map[x][y][z]


def executar(x, y, z):
    """Devolve as coordenadas da casa achada em (x, y, z) num mapa 2x3x4.
    Ponto de entrada publico desta unidade."""
    world = World(2, 3, 4)
    world.generate_world_map()
    return world.get_location(x, y, z).location
