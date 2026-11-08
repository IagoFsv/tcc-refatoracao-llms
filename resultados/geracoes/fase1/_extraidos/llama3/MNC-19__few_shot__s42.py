class Location:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class World:
    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.tamanho_x = tamanho_x
        self.tamanho_y = tamanho_y
        self.tamanho_z = tamanho_z
        self.world_map = self.generate_world_map()

    def generate_world_map(self):
        return [[[Location(x, y, z) for z in range(self.tamanho_z)] for y in range(self.tamanho_y)] for x in range(self.tamanho_x)]

    def get_location(self, x, y, z):
        return self.world_map[x][y][z].location


def executar(x, y, z):
    return World(2, 3, 4).get_location(x, y, z)
