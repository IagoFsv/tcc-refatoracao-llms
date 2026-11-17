class Location:
    """A map cell, identified by its coordinates."""

    def __init__(self, x, y, z):
        self.location = (x, y, z)


class Layer:
    """A 2D map of a specific z-coordinate."""

    def __init__(self, size_x, size_y):
        self.layer_map = [[Location(x, y, z) for y in range(size_y)] for x in range(size_x)]

    def get_location(self, x, y):
        return self.layer_map[x][y]


class World:
    def __init__(self, size_x, size_y, size_z):
        self.world_layers = [Layer(size_x, size_y) for _ in range(size_z)]

    def get_location(self, x, y, z):
        return self.world_layers[z].get_location(x, y)


def run(x, y, z):
    """Returns the coordinates of the cell found at (x, y, z) in a 2 x 3 x 4 map.
    Public entry point of this unit."""
    return World(2, 3, 4).get_location(x, y, z).location
