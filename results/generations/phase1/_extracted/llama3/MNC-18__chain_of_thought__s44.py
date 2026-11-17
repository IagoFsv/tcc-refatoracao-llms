class MapCell:
    def __init__(self, x, y, z):
        self.location = (x, y, z)
        self.terrain = None

    def generate_terrain(self):
        self.terrain = "grass"


class Map:
    def __init__(self, size_x, size_y, size_z):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.cells = [[MapCell(x, y, z) for z in range(size_z)] for y in range(size_y)] for x in range(size_x)

    def generate_terrain(self, x, y, z):
        self.cells[x][y][z].generate_terrain()


class TerrainGenerator:
    def generate_terrain(world, x, y, z):
        world.cells[x][y][z].generate_terrain()


def run(x, y, z):
    world = Map(2, 3, 4)
    TerrainGenerator.generate_terrain(world, x, y, z)
    return [cell.location for plane in world.cells for row in plane for cell in row
            if cell.terrain is not None]

"""Public entry point: run(x, y, z). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

print(run(1, 2, 3))  # Should output [(1, 2, 3)]
