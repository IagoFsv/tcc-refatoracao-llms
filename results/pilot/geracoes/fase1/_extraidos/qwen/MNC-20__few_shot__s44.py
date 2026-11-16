class Location:
    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class Plane:
    def __init__(self, fileiras):
        self.plane = [[Location(texto) for texto in fileira] for fileira in fileiras]


class Row:
    def __init__(self, descricoes):
        self.row = [Plane(descricoes)]


class World:
    def __init__(self, descricoes):
        self.world_map = [Row(descricoes)]
        self.world_map_size_x = 1
        self.world_map_size_y = 1
        self.world_map_size_z = len(descricoes[0][0])

    def get_location(self, x, y, z):
        return self.world_map[x].row[y].plane[z]


def render_scene(world):
    scene = [[["" for z in range(world.world_map_size_z)] for y in range(world.world_map_size_y)] for x in range(world.world_map_size_x)]

    for x in range(world.world_map_size_x):
        for y in range(world.world_map_size_y):
            for z in range(world.world_map_size_z):
                scene[x][y][z] = world.get_location(x, y, z).get_description()

    for x in range(world.world_map_size_x):
        for y in range(world.world_map_size_y):
            for z in range(world.world_map_size_z):
                print(scene[x][y][z], end="")
            print("")
    print("")


def executar(descricoes):
    render_scene(World(descricoes))
