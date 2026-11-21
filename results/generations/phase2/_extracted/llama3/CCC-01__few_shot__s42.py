"""Three-dimensional map of an adventure game: building the grid of cells.

Public entry point: run(size_x, size_y, size_z). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""


class Location:
    """A map cell, identified by its coordinates."""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.location = (x, y, z)


class World:
    def __init__(self, size_x, size_y, size_z):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.size = size_x * size_y * size_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [[[Location(x, y, z) for z in range(self.size_z)] for y in range(self.size_y)] for x in range(self.size_x)]


def run(size_x, size_y, size_z):
    """Builds a map of the given size and returns the coordinates of each cell,
    grouped by x and then by y. Public entry point of this unit."""
    world = World(size_x, size_y, size_z)
    planes = []
    for plane in world.world_map:
        rows = []
        for row in plane:
            rows.append([cell.location for cell in row])
        planes.append(rows)
    return planes
