class Location:
    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class World:
    def __init__(self, descricoes):
        self.world_map = self.create_map(descricoes)
        self.world_map_size_x, self.world_map_size_y, self.world_map_size_z = self.get_map_size(descricoes)

    def create_map(self, descricoes):
        return [[[Location(texto) for texto in fileira] for fileira in plano] for plano in descricoes]

    def get_map_size(self, descricoes):
        primeiro_plano = descricoes[0]
        return len(descricoes), len(primeiro_plano), len(primeiro_plano[0])

    def get_location(self, x, y, z):
        plano = self.world_map[x]
        return plano[y][z]


def render_scene(world):
    print("\n" * 100)
    scene = world.create_scene()
    world.print_scene(scene)


World.create_scene = lambda self: [[[self.get_location(x, y, z).get_description() for z in range(self.world_map_size_z)] for y in range(self.world_map_size_y)] for x in range(self.world_map_size_x)]
World.print_scene = lambda self, scene: print('\n'.join([''.join(map(str, row)) for row in scene]))


def executar(descricoes):
    render_scene(World(descricoes))
