from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class Location:
    """Uma casa do mapa; o terreno so existe depois de gerado."""
    location: Tuple[int, int, int]
    terrain: str = None

    def generate_terrain(self):
        self.terrain = "grass"

@dataclass
class World:
    world_map_size_x: int
    world_map_size_y: int
    world_map_size_z: int
    world_map: List[List[List[Location]]] = field(init=False)

    def generate_world_map(self):
        self.world_map = [[[Location(x, y, z) for z in range(self.world_map_size_z)] for y in range(self.world_map_size_y)] for x in range(self.world_map_size_x)]

def generate_terrain(world: World, x: int, y: int, z: int):
    """Gera o terreno na posicao (x, y, z) de um mapa 2 x 3 x 4 e devolve as
    posicoes que tem terreno. Ponto de entrada publico desta unidade."""
    world.world_map[x][y][z].generate_terrain()

def executar(x: int, y: int, z: int) -> List[Tuple[int, int, int]]:
    """Gera o terreno na posicao (x, y, z) de um mapa 2 x 3 x 4 e devolve as
    posicoes que tem terreno. Ponto de entrada publico desta unidade."""
    mundo = World(2, 3, 4)
    mundo.generate_world_map()
    generate_terrain(mundo, x, y, z)
    return [casa.location for plano in mundo.world_map for fileira in plano for casa in fileira
            if casa.terrain is not None]
