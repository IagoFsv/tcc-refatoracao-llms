from typing import List, Tuple

class Location:
    def __init__(self, x: int, y: int, z: int):
        self.location = (x, y, z)
        self.terrain = None

    def generate_terrain(self):
        self.terrain = "grass"

class World:
    def __init__(self, size_x: int, size_y: int, size_z: int):
        self.world_map_size_x = size_x
        self.world_map_size_y = size_y
        self.world_map_size_z = size_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [[[Location(x, y, z) for z in range(self.world_map_size_z)] for y in range(self.world_map_size_y)] for x in range(self.world_map_size_x)]

def generate_terrain(world: World, x: int, y: int, z: int):
    world.world_map[x][y][z].generate_terrain()

def run(x: int, y: int, z: int) -> List[Tuple[int, int, int]]:
    world = World(2, 3, 4)
    generate_terrain(world, x, y, z)
    return [cell.location for plane in world.world_map for row in plane for cell in row if cell.terrain is not None]
