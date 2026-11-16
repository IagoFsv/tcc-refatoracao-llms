class Location:
    """Uma casa do mapa, com a descricao que aparece na cena."""

    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class Plane:
    """Uma planilha 2D no mapa, com descricoes em cada linha."""

    def __init__(self, descriptions):
        self.locations = [Location(texto) for texto in descriptions]

    def get_location(self, y, z):
        return self.locations[z]


class Row:
    """Uma linha 1D no mapa, com descricoes em cada coluna."""

    def __init__(self, descriptions):
        self.locations = [Location(texto) for texto in descriptions]


class World:
    """Mapa montado a partir das descricoes: descricoes[x][y][z].

    O tamanho em cada eixo vem do primeiro elemento; se as fileiras tiverem
    tamanhos diferentes, o mapa fica irregular.
    """

    def __init__(self, descricoes):
        self.planes = [Plane(planos) for planos in descricoes]
        self.world_map_size_x = len(descricoes)
        self.world_map_size_y = len(descricoes[0])
        self.world_map_size_z = len(descricoes[0][0])

    def get_location(self, x, y, z):
        plane = self.planes[x]
        return plane.get_location(y, z)


def render_scene(world):
    """Render the current scene."""
    print("\n" * 100)

    # Print out the world map
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
    """Desenha a cena do mapa descrito. Ponto de entrada publico desta unidade."""
    render_scene(World(descricoes))
