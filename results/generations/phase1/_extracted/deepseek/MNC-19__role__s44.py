class Location:
    """A map cell, identified by its coordinates."""

    def __init__(self, x, y, z):
        self.coordinates = (x, y, z)


class World:
    def __init__(self, size_x, size_y, size_z):
        self.size = (size_x, size_y, size_z)
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = self.generate_map()

    def generate_map(self):
        return [[[Location(x, y, z) for z in range(self.size[2])] for y in range(self.size[1])] for x in range(self.size[0])]

    def get_location(self, x, y, z):
        return self.world_map[x][y][z]


def run(x, y, z):
    """Returns the coordinates of the cell found at  (x, y, z) in a 2 x 3 x 4 map.
    Public entry point of this unit."""
    return World(2, 3, 4).get_location(x, y, z).coordinates
