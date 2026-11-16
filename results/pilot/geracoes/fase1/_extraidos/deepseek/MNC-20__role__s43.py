class Location:
    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class World:
    def __init__(self, descricoes):
        self.locations = [Location(texto) for plano in descricoes for fileira in plano for texto in fileira]
        self.world_map_size_x = len(descricoes)
        self.world_map_size_y = len(descricoes[0])
        self.world_map_size_z = len(descricoes[0][0])

    def get_location(self, x, y, z):
        index = (x * self.world_map_size_y * self.world_map_size_z) + (y * self.world_map_size_z) + z
        return self.locations[index]


def render_scene(world):
    print("\n" * 100)
    scene = [["".join(world.get_location(x, y, z).get_description() for z in range(world.world_map_size_z)) for y in range(world.world_map_size_y)] for x in range(world.world_map_size_x)]
    for x in range(world.world_map_size_x):
        for y in range(world.world_map_size_y):
            print(scene[x][y])
    print("")


def executar(descricoes):
    render_scene(World(descricoes))
