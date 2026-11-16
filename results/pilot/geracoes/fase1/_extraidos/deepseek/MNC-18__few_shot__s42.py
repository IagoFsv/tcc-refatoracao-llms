"""Mapa tridimensional de um jogo de aventura: geracao do terreno da posicao atual.

Ponto de entrada publico: executar(x, y, z). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

from typing import Tuple, List

class Location:
    """Uma casa do mapa; o terreno so existe depois de gerado."""

    def __init__(self, x: int, y: int, z: int):
        self.location = (x, y, z)
        self.terrain = None

    def generate_terrain(self):
        self.terrain = "grass"


class World:
    def __init__(self, tamanho_x: int, tamanho_y: int, tamanho_z: int):
        self.world_map_size_x = tamanho_x
        self.world_map_size_y = tamanho_y
        self.world_map_size_z = tamanho_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = [[[Location(x, y, z) for z in range(self.world_map_size_z)] for y in range(self.world_map_size_y)] for x in range(self.world_map_size_x)]


def generate_terrain(world: World, x: int, y: int, z: int):
    """Gera o terreno na posicao  (x, y, z) de um mapa 2 x 3 x 4 e devolve as
    posicoes que tem terreno. Ponto de entrada publico desta unidade."""
    world.world_map[x][y][z].generate_terrain()


def executar(x: int, y: int, z: int) -> List[Tuple[int, int, int]]:
    """Gera o terreno na posicao  (x, y, z) de um mapa 2 x 3 x 4 e devolve as
    posicoes que tem terreno. Ponto de entrada publico desta unidade."""
    mundo = World(2, 3, 4)
    generate_terrain(mundo, x, y, z)
    return [casa.location for plano in mundo.world_map for fileira in plano for casa in fileira if casa.terrain is not None]
