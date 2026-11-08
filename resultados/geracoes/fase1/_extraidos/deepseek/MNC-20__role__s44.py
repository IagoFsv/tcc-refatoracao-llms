class Location:
    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class Plane:
    def __init__(self, descriptions):
        self.planes = [Location(description) for description in descriptions]


class World:
    def __init__(self, descriptions):
        self.world_map = [Plane(plane_descriptions) for plane_descriptions in descriptions]

    def get_location(self, x, y, z):
        return self.world_map[x].planes[y].get_description()


def render_scene(world):
    print("\n" * 100)

    for x in range(len(world.world_map)):
        for y in range(len(world.world_map[x].planes)):
            print(world.get_location(x, y, 0), end="")
        print("")
    print("")


def executar(descricoes):
    render_scene(World(descricoes))
