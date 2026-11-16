class Location:
    def  __init__(self, x, y, z):
        self.location = (x, y, z)


class World:
    def  __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.world_map_size_x = tamanho_x
        self.world_map_size_y = tamanho_y
        self.world_map_size_z = tamanho_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [[[Location(x, y, z) for z in range(self.world_map_size_z)] for y in range(self.world_map_size_y)] for x in range(self.world_map_size_x)]

    def get_location(self, x, y, z):
        return self.world_map[x][y][z]


class GameWorld:
    def __init__(self, x, y, z):
        self.world = World(x, y, z)

    def get_location(self, x, y, z):
        return self.world.get_location(x, y, z)


def executar(x, y, z):
    return GameWorld(2, 3, 4).get_location(x, y, z).location
