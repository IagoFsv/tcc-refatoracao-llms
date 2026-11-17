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
    def __init__(self, size_y, size_z):
        self.plane = [[Location(x, y, z) for z in range(size_z)] for y in range(size_y)]

    def generate_plane(self):
        for row in self.plane:
            for cell in row:
                cell.generate_terrain()


class Row:
    def __init__(self, size_z):
        self.row = [Location(x, y, z) for z in range(size_z)]

    def generate_row(self):
        for cell in self.row:
            cell.generate_terrain()


class World:
    def __init__(self, size_x, size_y, size_z):
        self.world_map_size_x = size_x
        self.world_map_size_y = size_y
        self.world_map_size_z = size_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [Plane(self.world_map_size_y, self.world_map_size_z) for x in range(self.world_map_size_x)]
        for plane in self.world_map:
            plane.generate_plane()


def generate_terrain(world, x, y, z):
    world.world_map[x].plane[y].row[z].generate_terrain()


def run(x, y, z):
    """Public entry point of this unit.

    Generates the terrain at position (x, y, z) of a 2 x 3 x 4 map and returns
    the positions that have terrain.
    """
    world = World(2, 3, 4)
    generate_terrain(world, x, y, z)
    return [cell.location for plane in world.world_map for row in plane.plane for cell in row.row
            if cell.terrain is not None]
