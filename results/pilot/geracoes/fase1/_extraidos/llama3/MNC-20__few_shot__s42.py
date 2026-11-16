from dataclasses import dataclass

@dataclass
class Location:
    description: str

@dataclass
class WorldMap:
    locations: list[list[list[Location]]]

@dataclass
class World:
    world_map: WorldMap

def render_scene(world: World):
    """Render the current scene."""
    print("\n" * 100)

    scene = [["" for _ in range(world.world_map.locations[0][0].__len__())] for _ in range(world.world_map.locations.__len__())]

    for x in range(world.world_map.locations.__len__()):
        for y in range(world.world_map.locations[0].__len__()):
            for z in range(world.world_map.locations[0][0].__len__()):
                scene[x][y][z] = world.world_map.locations[x][y][z].description

    for x in range(world.world_map.locations.__len__()):
        for y in range(world.world_map.locations[0].__len__()):
            for z in range(world.world_map.locations[0][0].__len__()):
                print(scene[x][y][z], end="")
            print("")
    print("")


def executar(descricoes):
    """Desenha a cena do mapa descrito. Ponto de entrada publico desta unidade."""
    world_map = WorldMap([[[Location(texto) for texto in fileira] for fileira in plano] for plano in descricoes])
    render_scene(World(world_map))
