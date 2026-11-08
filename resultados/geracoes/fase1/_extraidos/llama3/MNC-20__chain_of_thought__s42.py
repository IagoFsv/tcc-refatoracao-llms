class Location:
    """Uma casa do mapa, com a descricao que aparece na cena."""

    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class WorldMap:
    """Representa o mapa do mundo."""

    def __init__(self, descricoes):
        self.map_size_x = len(descricoes)
        self.map_size_y = len(descricoes[0])
        self.map_size_z = len(descricoes[0][0])

    def get_location(self, x, y, z):
        raise NotImplementedError


class LocationMap(WorldMap):
    """Representa a descrição de uma localização no mapa."""

    def __init__(self, descricoes):
        super().__init__(descricoes)
        self.locations = [[[Location(texto) for texto in fileira] for fileira in plano] for plano in descricoes]

    def get_location(self, x, y, z):
        return self.locations[x][y][z]


def render_scene(world):
    """Render the current scene."""
    print("\n" * 100)

    # Print out the world map
    scene = []
    for x in range(world.map_size_x):
        row = []
        for y in range(world.map_size_y):
            row.append([])
            for z in range(world.map_size_z):
                row[y].append(world.get_location(x, y, z).get_description())
        scene.append(row)

    for row in scene:
        for cell in row:
            print(" ".join(cell))
        print()


def executar(descricoes):
    """Desenha a cena do mapa descrito. Ponto de entrada publico desta unidade."""
    world = LocationMap(descricoes)
    render_scene(world)
