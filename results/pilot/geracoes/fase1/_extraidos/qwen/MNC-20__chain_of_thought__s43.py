class Location:
    """Uma casa do mapa, com a descrição que aparece na cena."""

    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class Row:
    """Uma linha no plano do mapa."""

    def __init__(self, locations):
        self.locations = locations

    def get_location(self, y, z):
        return self.locations[y][z]


class Plane:
    """Um plano no mundo do mapa."""

    def __init__(self, rows):
        self.rows = rows

    def get_location(self, y, z):
        return self.rows[y].get_location(y, z)


class World:
    """Mapa montado a partir das descricoes: descricoes[x][y][z].

    O tamanho em cada eixo vem do primeiro elemento; se as fileiras tiverem
    tamanhos diferentes, o mapa fica irregular.
    """

    def __init__(self, descricoes):
        self.world_map = []
        for plano in descricoes:
            rows = []
            for fileira in plano:
                locations = []
                for texto in fileira:
                    locations.append(Location(texto))
                rows.append(Row(locations))
            self.world_map.append(Plane(rows))

        primeiro_plano = descricoes[0]
        self.world_map_size_x = len(descricoes)
        self.world_map_size_y = len(primeiro_plano)
        self.world_map_size_z = len(primeiro_plano[0])

    def get_location(self, x, y, z):
        plano = self.world_map[x]
        return plano.get_location(y, z)


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
