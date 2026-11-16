class Location:
    """Uma casa do mapa, com a descricao que aparece na cena."""

    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class World:
    """Mapa montado a partir das descricoes: descricoes[x][y][z].

    O tamanho em cada eixo vem do primeiro elemento; se as fileiras tiverem
    tamanhos diferentes, o mapa fica irregular.
    """

    def __init__(self, descricoes):
        self.world_map = descricoes
        self.world_map_size_x = len(self.world_map)
        self.world_map_size_y = len(self.world_map[0])
        self.world_map_size_z = len(self.world_map[0][0])

    def get_location(self, x, y, z):
        return self.world_map[x][y][z]


def render_scene(world):
    """Render the current scene."""
    print("\n" * 100)


    # Print out the world map
    for x in range(world.world_map_size_x):
        for y in range(world.world_map_size_y):
            for z in range(world.world_map_size_z):
                print(world.get_location(x, y, z).get_description(), end="")
            print("")
    print("")


def executar(descricoes):
    """Desenha a cena do mapa descrito. Ponto de entrada publico desta unidade."""
    world = World(descricoes)
    render_scene(world)
