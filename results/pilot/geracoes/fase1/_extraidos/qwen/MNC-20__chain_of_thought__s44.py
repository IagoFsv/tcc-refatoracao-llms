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
        self.x_size = len(descricoes)
        self.y_size = len(descricoes[0])
        self.z_size = len(descricoes[0][0])
        self.world_map = [
            [
                [Location(texto) for texto in fileira] for fileira in plano
            ] for plano in descricoes
        ]

    def get_location(self, x, y, z):
        return self.world_map[x][y][z]


def render_scene(world):
    """Render the current scene."""
    print("\n" * 100)

    # Print out the world map
    scene = [
        [
            ["" for z in range(world.z_size)] for y in range(world.y_size)
        ] for x in range(world.x_size)
    ]

    for x in range(world.x_size):
        for y in range(world.y_size):
            for z in range(world.z_size):
                scene[x][y][z] = world.get_location(x, y, z).get_description()

    for x in range(world.x_size):
        for y in range(world.y_size):
            for z in range(world.z_size):
                print(scene[x][y][z], end="")
            print("")
    print("")


def executar(descricoes):
    """Desenha a cena do mapa descrito. Ponto de entrada publico desta unidade."""
    render_scene(World(descricoes))
