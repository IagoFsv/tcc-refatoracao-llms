"""Three-dimensional map of an adventure game: terrain generation at the current position.

Public entry point: run(x, y, z). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""


class Location:
    """A map cell; the terrain only exists after it is generated."""

    def __init__(self, x, y, z):
        self.location = (x, y, z)
        self.terrain = None

    def generate_terrain(self):
        self.terrain = "grass"


class Plane:
    """A 2D map cell; the terrain only exists after it is generated."""

    def __init__(self, y, z):
        self.plane = [(Location(x, y, z) for z in range(4)) for x in range(2)]

    def generate_terrain(self, x):
        self.plane[x].generate_terrain()


class World:
    def __init__(self, size_x, size_y, size_z):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.generate_world_map()

    def generate_world_map(self):
        self.plane_map = [Plane(y, self.size_z) for y in range(self.size_y)]

    def generate_terrain(self, x, y, z):
        self.plane_map[y].generate_terrain(x)


def run(x, y, z):
    """Public entry point of this unit.

    Generates the terrain at position (x, y, z) of a 2 x 3 x 4 map and returns
    the positions that have terrain.
    """
    world = World(2, 3, 4)
    world.generate_terrain(x, y, z)
    return [cell.location for plane in world.plane_map for row in plane for cell in row
            if cell.terrain is not None]
