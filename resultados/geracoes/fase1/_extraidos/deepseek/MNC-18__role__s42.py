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
        self.world_map = self.generate_world_map()

    def generate_world_map(self):
        return [[[Location(x, y, z) for z in range(self.world_map_size_z)] for y in range(self.world_map_size_y)] for x in range(self.world_map_size_x)]

    def generate_terrain(self, x, y, z):
        self.world_map[x][y][z].generate_terrain()


def execute(x, y, z):
    world = World(2, 3, 4)
    world.generate_terrain(x, y, z)
    return [location.location for plane in world.world_map for row in plane for location in row if location.terrain is not None]
