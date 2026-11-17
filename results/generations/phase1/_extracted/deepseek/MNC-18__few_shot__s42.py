"""Three-dimensional map of an adventure game: terrain generation at the current position.

Public entry point: run(x, y, z). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class Location:
    """A map cell; the terrain only exists after it is generated."""
    location: Tuple[int, int, int]
    terrain: str = None

@dataclass
class World:
    world_map_size_x: int
    world_map_size_y: int
    world_map_size_z: int
    world_map: List[List[List[Location]]] = field(init=False)

    def generate_world_map(self):
        self.world_map = [[[Location(x, y, z) for z in range(self.world_map_size_z)] for y in range(self.world_map_size_y)] for x in range(self.world_map_size_x)]

def generate_terrain(world: World, x: int, y: int, z: int):
    world.world_map[x][y][z].terrain = "grass"

def run(x: int, y: int, z: int) -> List[Tuple[int, int, int]]:
    """Public entry point of this unit.

    Generates the terrain at position  (x, y, z) of a 2 x 3 x 4 map and returns
    the positions that have terrain.
    """
    world = World(2, 3, 4)
    world.generate_world_map()
    generate_terrain(world, x, y, z)
    return [cell.location for plane in world.world_map for row in plane for cell in row
            if cell.terrain is not None]
