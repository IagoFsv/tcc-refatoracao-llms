from dataclasses import dataclass
from typing import Tuple

@dataclass
class Coordinates:
    x: int
    y: int
    z: int

@dataclass
class Location:
    """A map cell, identified by its coordinates."""

    coordinates: Coordinates


class World:
    def __init__(self, size_x: int, size_y: int, size_z: int):
        self.world_map_size_x = size_x
        self.world_map_size_y = size_y
        self.world_map_size_z = size_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [[[Location(Coordinates(x, y, z)) for z in range(self.world_map_size_z)] for y in range(self.world_map_size_y)] for x in range(self.world_map_size_x)]

    def get_location(self, x: int, y: int, z: int) -> Location:
        return self.world_map[x][y][z]


def run(x: int, y: int, z: int) -> Tuple[int, int, int]:
    """Returns the coordinates of the cell found at 
    (x, y, z) in a 2 x 3 x 4 map.
    Public entry point of this unit."""
    return World(2, 3, 4).get_location(x, y, z).coordinates
