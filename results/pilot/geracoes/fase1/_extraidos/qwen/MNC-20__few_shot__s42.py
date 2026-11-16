class Location:
    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class Plane:
    def __init__(self, fileiras):
        self.fileiras = fileiras

    def get_fileira(self, y):
        return self.fileiras[y]


class Row:
    def __init__(self, descricoes):
        self.descricoes = descricoes

    def get_location(self, z):
        return Location(self.descricoes[z])


class World:
    def __init__(self, descricoes):
        self.planos = [Plane([Row(fileira) for fileira in plano]) for plano in descricoes]
        self.world_map_size_x = len(descricoes)
        self.world_map_size_y = len(descricoes[0])
        self.world_map_size_z = len(descricoes[0][0])

    def get_location(self, x, y, z):
        plano = self.planos[x]
        fileira = plano.get_fileira(y)
        return fileira.get_location(z)


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
