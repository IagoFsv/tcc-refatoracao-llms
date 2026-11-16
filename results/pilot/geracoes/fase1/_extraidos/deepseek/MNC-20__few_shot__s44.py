from dataclasses import dataclass, field
from typing import List

@dataclass
class Location:
    description: str

@dataclass
class World:
    world_map: List[List[List[Location]]]
    world_map_size_x: int
    world_map_size_y: int
    world_map_size_z: int

    def get_location(self, x: int, y: int, z: int) -> Location:
        return self.world_map[x][y][z]


def render_scene(world: World):
    print("\n" * 100)

    # Print out the world map
    scene = [[["" for _ in range(world.world_map_size_z)] for _ in range(world.world_map_size_y)] for _ in range(world.world_map_size_x)]

    for x in range(world.world_map_size_x):
        for y in range(world.world_map_size_y):
            for z in range(world.world_map_size_z):
                scene[x][y][z] = world.get_location(x, y, z).description

    for x in range(world.world_map_size_x):
        for y in range(world.world_map_size_y):
            for z in range(world.world_map_size_z):
                print(scene[x][y][z], end="")
            print("")
    print("")


def executar(descricoes):
    world = World(
        world_map=[[[Location(texto) for texto in fileira] for fileira in plano] for plano in descricoes],
        world_map_size_x=len(descricoes),
        world_map_size_y=len(descricoes[0]),
        world_map_size_z=len(descricoes[0][0])
    )
    render_scene(world)
