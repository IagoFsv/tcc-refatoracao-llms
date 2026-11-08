class Location:
    """Uma casa do mapa, com a descrição que aparece na cena."""

    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class Row:
    """Uma linha de uma plano no mapa."""

    def __init__(self, locations):
        self.locations = locations

    def get_location(self, x):
        return self.locations[x]


class Plane:
    """Um plano do mapa."""

    def __init__(self, rows):
        self.rows = rows

    def get_location(self, x, y):
        return self.rows[y].get_location(x)


class World:
    """Mapa montado a partir das descricoes: descricoes[x][y][z].

    O tamanho em cada eixo vem do primeiro elemento; se as fileiras tiverem
    tamanhos diferentes, o mapa fica irregular.
    """

    def __init__(self, descricoes):
        self.planes = [
            Plane([
                Row([Location(texto) for texto in fileira])
                for fileira in plano
            ])
            for plano in descricoes
        ]
        self.world_map_size_x = len(descricoes)
        self.world_map_size_y = len(descricoes[0]) if descricoes else 0
        self.world_map_size_z = len(descricoes[0][0]) if descricoes and descricoes[0] else 0

    def get_location(self, x, y, z):
        return self.planes[z].get_location(x, y)


def render_scene(world):
    """Render the current scene."""
    print("\n" * 100)

    # Print out the world map
    scene = [
        [
            ["" for z in range(world.world_map_size_z)]
            for y in range(world.world_map_size_y)
        ]
        for x in range(world.world_map_size_x)
    ]

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
