class Location:
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
        self.world_map = {(x, y, z): Location(x, y, z) for x in range(self.world_map_size_x) for y in range(self.world_map_size_y) for z in range(self.world_map_size_z)}

    def get_location(self, x, y, z):
        return self.world_map[(x, y, z)]


def generate_terrain(world, x, y, z):
    location = world.get_location(x, y, z)
    location.generate_terrain()


def run(x, y, z):
    """Public entry point of this unit.

    Generates the terrain at position  (x, y, z) of a 2 x 3 x 4 map and returns
    the positions that have terrain.
    """
    world = World(2, 3, 4)
    generate_terrain(world, x, y, z)
    return [cell.location for cell in world.world_map.values() if cell.terrain is not None]
