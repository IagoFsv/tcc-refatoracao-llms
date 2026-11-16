from dataclasses import dataclass

@dataclass
class Location:
    x: int
    y: int
    z: int

@dataclass
class World:
    tamanho_x: int
    tamanho_y: int
    tamanho_z: int

    def __init__(self, tamanho_x: int, tamanho_y: int, tamanho_z: int):
        self.tamanho_x = tamanho_x
        self.tamanho_y = tamanho_y
        self.tamanho_z = tamanho_z
        self.world_map = [[[(x, y, z) for z in range(tamanho_z)] for y in range(tamanho_y)] for x in range(tamanho_x)]

    def get_location(self, x: int, y: int, z: int) -> tuple:
        return self.world_map[x][y][z]

def executar(x: int, y: int, z: int) -> tuple:
    return World(2, 3, 4).get_location(x, y, z)
