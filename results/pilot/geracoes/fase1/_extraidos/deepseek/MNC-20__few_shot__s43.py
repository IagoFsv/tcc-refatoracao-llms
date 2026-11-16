from typing import List

class Description:
    def __init__(self, text: str):
        self.text = text

class Location:
    def __init__(self, description: Description):
        self.description = description

    def get_description(self):
        return self.description.text

class World:
    def __init__(self, descriptions: List[List[List[str]]]):
        self.world_map = [[[Location(Description(text)) for text in layer] for layer in plane] for plane in descriptions]
        self.world_map_size_x = len(descriptions)
        self.world_map_size_y = len(descriptions[0])
        self.world_map_size_z = len(descriptions[0][0])

    def get_location(self, x: int, y: int, z: int):
        plane = self.world_map[x]
        return plane[y][z]

def render_scene(world: World):
    print("\n" * 100)

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

def executar(descricoes: List[List[List[str]]]):
    render_scene(World(descricoes))
