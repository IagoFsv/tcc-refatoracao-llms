from dataclasses import dataclass

@dataclass
class Location:
    x: int
    y: int
    z: int
    terrain: str = None

@dataclass
class World:
    tamanho_x: int
    tamanho_y: int
    tamanho_z: int

    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.tamanho_x = tamanho_x
        self.tamanho_y = tamanho_y
        self.tamanho_z = tamanho_z
        self.world_map = [[Location(x, y, z) for z in range(tamanho_z)] for y in range(tamanho_y) for x in range(tamanho_x)]

    def generate_terrain(self, x, y, z):
        self.world_map[x][y][z].terrain = "grass"

def executar(x, y, z):
    mundo = World(2, 3, 4)
    mundo.generate_terrain(x, y, z)
    return [(x, y, z)] if mundo.world_map[x][y][z].terrain is not None else []
