class Location:
    def __init__(self, x, y, z):
        self.location = (x, y, z)
        self.terrain = None

    def generate_terrain(self):
        self.terrain = "grass"


class Plane:
    def __init__(self, tamanho_y, tamanho_z):
        self.plane = [[Location(x, y, z) for z in range(tamanho_z)] for y in range(tamanho_y)]

    def generate_plane(self):
        for linha in self.plane:
            for local in linha:
                local.generate_terrain()


class Row:
    def __init__(self, tamanho_z):
        self.row = [Location(x, y, z) for z in range(tamanho_z)]

    def generate_row(self):
        for local in self.row:
            local.generate_terrain()


class World:
    def __init__(self, tamanho_x, tamanho_y, tamanho_z):
        self.world_map_size_x = tamanho_x
        self.world_map_size_y = tamanho_y
        self.world_map_size_z = tamanho_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [Plane(self.world_map_size_y, self.world_map_size_z) for _ in range(self.world_map_size_x)]


def generate_terrain(mundo, x, y, z):
    mundo.world_map[x].plane[y].plane[z].generate_terrain()


def executar(x, y, z):
    mundo = World(2, 3, 4)
    generate_terrain(mundo, x, y, z)
    return [casa.location for plano in mundo.world_map for fileira in plano.plane for casa in fileira.row
            if casa.terrain is not None]
