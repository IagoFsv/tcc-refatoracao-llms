from dataclasses import dataclass

@dataclass
class Location:
    description: str

@dataclass
class WorldMap:
    locations: List[List[List[Location]]]

@dataclass
class World:
    world_map: WorldMap

@dataclass
class Scene:
    world_map: World
    scene: List[List[List[str]]]

def render_scene(world: World) -> None:
    scene = Scene(world, [[["" for _ in range(world.world_map.world_map_size_z)] for _ in range(world.world_map.world_map_size_y)] for _ in range(world.world_map.world_map_size_x)])

    for x in range(world.world_map.world_map_size_x):
        for y in range(world.world_map.world_map_size_y):
            for z in range(world.world_map.world_map_size_z):
                scene.scene[x][y][z] = world.world_map.locations[x][y][z].description

    for x in range(world.world_map.world_map_size_x):
        for y in range(world.world_map.world_map_size_y):
            for z in range(world.world_map.world_map_size_z):
                print(scene.scene[x][y][z], end="")
            print("")
    print("")


def executar(descricoes):
    world = World(WorldMap([[[Location(texto) for texto in fileira] for fileira in plano] for plano in descricoes]))
    render_scene(world)
