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
    world_map: list = None

    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.tamanho_x = tamanho_x
        self.tamanho_y = tamanho_y
        self.tamanho_z = tamanho_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [[Location(x, y, z) for z in range(self.tamanho_z)] for y in range(self.tamanho_y) for x in range(self.tamanho_x)]

    def generate_terrain(self, x, y, z):
        self.world_map[x][y][z].terrain = "grass"

    def executar(self, x, y, z):
        self.generate_terrain(x, y, z)
        return [(casa.x, casa.y, casa.z) for fileira in self.world_map for casa in fileira if casa.terrain is not None]
