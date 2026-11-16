class Location:
    """Uma casa do mapa, com a descricao que aparece na cena."""

    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class WorldMap:
    """Mapa montado a partir das descricoes: descricoes[x][y][z]."""

    def __init__(self, descricoes):
        self.map = [[[Location(texto) for texto in fileira] for fileira in plano] for plano in descricoes]
        self.size_x = len(descricoes)
        self.size_y = len(descricoes[0])
        self.size_z = len(descricoes[0][0])

    def get_location(self, x, y, z):
        return self.map[x][y][z].get_description()


class Scene:
    """Cena a ser renderizada."""

    def __init__(self, world_map):
        self.world_map = world_map

    def render(self):
        print("\n" * 100)

        for x in range(self.world_map.size_x):
            for y in range(self.world_map.size_y):
                for z in range(self.world_map.size_z):
                    print(self.world_map.get_location(x, y, z), end="")
                print("")
        print("")


def executar(descricoes):
    """Desenha a cena do mapa descrito. Ponto de entrada publico desta unidade."""
    world_map = WorldMap(descricoes)
    scene = Scene(world_map)
    scene.render()
