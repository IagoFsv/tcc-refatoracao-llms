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
    world_map: list[list[list[Location]]]

    def __init__(self, tamanho_x: int, tamanho_y: int, tamanho_z: int):
        self.tamanho_x = tamanho_x
        self.tamanho_y = tamanho_y
        self.tamanho_z = tamanho_z
        self.world_map = [[[Location(x, y, z) for z in range(tamanho_z)] for y in range(tamanho_y)] for x in range(tamanho_x)]

    def generate_terrain(self, x: int, y: int, z: int):
        self.world_map[x][y][z].terrain = "grass"

    def executar(self, x: int, y: int, z: int):
        self.generate_terrain(x, y, z)
        return [casa.location for plano in self.world_map for fileira in plano for casa in fileira
                if casa.terrain is not None]
