class Terrain:
    def __init__(self):
        self.terrain = None

    def generate_terrain(self):
        self.terrain = "grass"


class Location:
    def __init__(self, x, y, z):
        self.location = (x, y, z)
        self.terrain = Terrain()

    def generate_terrain(self):
        self.terrain.generate_terrain()


class World:
    def __init__(self, size_x, size_y, size_z):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.world_map = self.generate_world_map()

    def generate_world_map(self):
        return [[[Location(x, y, z) for z in range(self.size_z)] for y in range(self.size_y)] for x in range(self.size_x)]


def execute(x, y, z):
    world = World(2, 3, 4)
    location = world.world_map[x][y][z]
    location.generate_terrain()
    return [location.location for location in world.world_map[x][y] if location.terrain.terrain is not None]
