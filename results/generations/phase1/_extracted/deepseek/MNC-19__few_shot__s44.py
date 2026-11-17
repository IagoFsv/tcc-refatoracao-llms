from dataclasses import dataclass

@dataclass
class Coordinates:
    x: int
    y: int
    z: int

@dataclass
class Location:
    coordinates: Coordinates

class World:
    def __init__(self, size_x, size_y, size_z):
        self.world_map_size_x = size_x
        self.world_map_size_y = size_y
        self.world_map_size_z = size_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [[[Location(Coordinates(x, y, z)) for z in range(self.world_map_size_z)] for y in range(self.world_map_size_y)] for x in range(self.world_map_size_x)]

    def get_location(self, x, y, z):
        return self.world_map[x][y][z].coordinates


def run(x, y, z):
    return World(2, 3, 4).get_location(x, y, z)
