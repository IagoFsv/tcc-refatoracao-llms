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
        self.locations = [Location(texto) for plano in descricoes for fileira in plano for texto in fileira]
        self.world_map_size_x = len(descricoes)
        self.world_map_size_y = len(descricoes[0])
        self.world_map_size_z = len(descricoes[0][0])

    def get_location(self, x, y, z):
        index = z + self.world_map_size_z * (y + self.world_map_size_y * x)
        return self.locations[index]


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
    render_scene(World(descricoes))
