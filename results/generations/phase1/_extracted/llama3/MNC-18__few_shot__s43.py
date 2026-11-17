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
        self.world_map = self.generate_world_map()

    def generate_world_map(self):
        return [[[Location(x, y, z) for z in range(self.size_z)] for y in range(self.size_y)] for x in range(self.size_x)]


class WorldGenerator:
    def __init__(self, world):
        self.world = world

    def generate_terrain(self):
        for x in range(self.world.size_x):
            for y in range(self.world.size_y):
                for z in range(self.world.size_z):
                    self.world.world_map[x][y][z].generate_terrain()


def run(x, y, z):
    """Public entry point of this unit.

    Generates the terrain at position (x, y, z) of a 2 x 3 x 4 map and returns
    the positions that have terrain.
    """
    world = World(2, 3, 4)
    generator = WorldGenerator(world)
    generator.generate_terrain()
    return [(cell.location[0], cell.location[1], cell.location[2]) for plane in world.world_map for row in plane for cell in row
            if cell.terrain is not None]
