class Location:
    """A map cell; the terrain only exists after it is generated."""

    def __init__(self, x, y, z):
        self.location = (x, y, z)
        self.terrain = None

    def generate_terrain(self):
        self.terrain = "grass"


class World:
    def __init__(self, size_x, size_y, size_z):
        self.world_map_size_x = size_x
        self.world_map_size_y = size_y
        self.world_map_size_z = size_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [[[Location(x, y, z) for z in range(self.world_map_size_z)] for y in range(self.world_map_size_y)] for x in range(self.world_map_size_x)]

    def get_location(self, x, y, z):
        return self.world_map[x][y][z]


def run(x, y, z):
    """Public entry point of this unit.

    Generates the terrain at position  (x, y, z) of a 2 x 3 x 4 map and returns
    the positions that have terrain.
    """
    world = World(2, 3, 4)
    location = world.get_location(x, y, z)
    location.generate_terrain()
    return [cell.location for plane in world.world_map for row in plane for cell in row
            if cell.terrain is not None]
