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
        self.world_map = self._create_world_map(descricoes)
        self.world_map_size_x = len(descricoes)
        self.world_map_size_y = len(descricoes[0])
        self.world_map_size_z = len(descricoes[0][0])

    def _create_world_map(self, descricoes):
        return [[[Location(texto) for texto in fileira] for fileira in plano] for plano in descricoes]

    def get_location(self, x, y, z):
        return self.world_map[x][y][z]


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
