from dataclasses import dataclass

@dataclass
class Location:
    description: str

@dataclass
class World:
    descricoes: list[list[list[Location]]]

    def __init__(self, descricoes):
        self.descricoes = descricoes

    def get_location(self, x: int, y: int, z: int) -> Location:
        return self.descricoes[x][y][z]

def render_scene(world: World):
    """Render the current scene."""
    print("\n" * 100)

    for x in range(len(world.descricoes)):
        for y in range(len(world.descricoes[0])):
            for z in range(len(world.descricoes[0][0])):
                location = world.get_location(x, y, z)
                print(location.description, end="")
            print("")
    print("")

def executar(descricoes):
    """Desenha a cena do mapa descrito. Ponto de entrada publico desta unidade."""
    render_scene(World(descricoes))
