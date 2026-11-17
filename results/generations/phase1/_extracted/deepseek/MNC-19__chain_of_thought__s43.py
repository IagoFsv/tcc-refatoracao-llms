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
        self.world_map = [[[Location(x, y, z) for z in range(self.world_map_size_z)] for y in range(self.world_map_size_y)] for x in range(self.world_map_size_x)]


class LocationFinder:
    def __init__(self, world):
        self.world = world

    def get_location(self, x, y, z):
        return self.world.world_map[x][y][z]


def run(x, y, z):
    """Returns the coordinates of the cell found at  (x, y, z) in a 2 x 3 x 4 map.
    Public entry point of this unit."""
    world = World(2, 3, 4)
    location_finder = LocationFinder(world)
    return location_finder.get_location(x, y, z).location
