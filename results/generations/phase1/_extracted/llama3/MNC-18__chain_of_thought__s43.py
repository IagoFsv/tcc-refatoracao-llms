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


class World:
    def __init__(self, size_x, size_y, size_z):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.locations_x = [None] * size_x
        self.locations_y = [None] * size_y
        self.locations_z = [None] * size_z
        self.generate_world_map()

    def generate_world_map(self):
        self.locations_x = [self.locations_y[:] for _ in range(self.size_x)]
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.locations_x[i][j] = [self.locations_z[:] for _ in range(self.size_z)]
                for k in range(self.size_z):
                    self.locations_x[i][j][k] = Location(i, j, k)

    def generate_terrain(self, x, y, z):
        self.locations_x[x][y][z].generate_terrain()


def run(x, y, z):
    """Public entry point of this unit.

    Generates the terrain at position (x, y, z) of a 2 x 3 x 4 map and returns
    the positions that have terrain.
    """
    world = World(2, 3, 4)
    world.locations_x[x][y][z].generate_terrain()
    return [cell.location for i in range(world.size_x) for j in range(world.size_y) for k in range(world.size_z)
            if cell.terrain is not None]
