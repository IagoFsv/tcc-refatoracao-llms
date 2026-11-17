"""Three-dimensional map of an adventure game: looking up a position.

Public entry point: run(x, y, z). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Location:
    """A map cell, identified by its coordinates."""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class World:
    def __init__(self, size_x, size_y, size_z):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.world_map = self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [[{z: Location(x, y, z) for z in range(self.size_z)} for y in range(self.size_y)] for x in range(self.size_x)]

    def get_location(self, x, y, z):
        return self.world_map[x][y][z]


def run(x, y, z):
    """Returns the coordinates of the cell found at (x, y, z) in a 2 x 3 x 4 map.
    Public entry point of this unit."""
    return World(2, 3, 4).get_location(x, y, z)
