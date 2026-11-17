"""Three-dimensional map of an adventure game: looking up a position.

Public entry point: run(x, y, z). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

class Location:
    """A map cell, identified by its coordinates."""

    def __init__(self, x, y, z):
        self.location = (x, y, z)


class World:
    def __init__(self, size_x, size_y, size_z):
        self.world_map_size_x = size_x
        self.world_map_size_y = size_y
        self.world_map_size_z = size_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = self.create_3d_map()

    def create_3d_map(self):
        map_2d = []
        for x in range(self.world_map_size_x):
            map_1d = []
            for y in range(self.world_map_size_y):
                map_1d.append(self.create_2d_layer(x, y))
            map_2d.append(map_1d)
        return map_2d

    def create_2d_layer(self, x, y):
        layer = []
        for z in range(self.world_map_size_z):
            layer.append(Location(x, y, z))
        return layer

    def get_location(self, x, y, z):
        return self.world_map[x][y][z]


def run(x, y, z):
    """Returns the coordinates of the cell found at (x, y, z) in a 2 x 3 x 4 map.
    Public entry point of this unit."""
    return World(2, 3, 4).get_location(x, y, z).location
