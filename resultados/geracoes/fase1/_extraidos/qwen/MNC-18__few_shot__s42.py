class Location:
    def __init__(self, x, y, z):
        self.location = (x, y, z)
        self.terrain = None

    def generate_terrain(self):
        self.terrain = "grass"


class Plane:
    def __init__(self, tamanho_z):
        self.plane = [Location(0, 0, z) for z in range(tamanho_z)]


class Row:
    def __init__(self, tamanho_y, tamanho_z):
        self.row = [Plane(tamanho_z) for _ in range(tamanho_y)]


class World:
    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.tamanho_x = tamanho_x
        self.tamanho_y = tamanho_y
        self.tamanho_z = tamanho_z
        self.world_map = self.generate_world_map()

    def generate_world_map(self):
        return [Row(self.tamanho_y, self.tamanho_z) for _ in range(self.tamanho_x)]


def executar(x, y, z):
    mundo = World(2, 3, 4)
    mundo.world_map[x].row[y].plane[z].generate_terrain()
    return [(x, y, z) for plano in mundo.world_map for fileira in plano.plane for casa in fileira.plane
            if casa.terrain is not None]
