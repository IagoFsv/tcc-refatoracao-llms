from dataclasses import dataclass
from typing import List

@dataclass
class Location:
    """A map cell, with the description that appears in the scene."""
    description: str

@dataclass
class World:
    """Map built from the descriptions: descriptions[x][y][z].

    The size on each axis comes from the first element; if the rows have
    different sizes, the map is irregular.
    """
    world_map: List[List[List[Location]]]
    world_map_size_x: int
    world_map_size_y: int
    world_map_size_z: int

    def __init__(self, descriptions):
        self.world_map = [[[Location(text) for text in row] for row in plane] for plane in descriptions]
        first_plane = descriptions[0]
        self.world_map_size_x = len(descriptions)
        self.world_map_size_y = len(first_plane)
        self.world_map_size_z = len(first_plane[0])

    def get_location(self, x, y, z):
        plane = self.world_map[x]
        return plane[y][z]


def render_scene(world):
    """Render the current scene."""
    print("\n" * 100)

    # Print out the world map
    scene = [[["" for z in range(world.world_map_size_z)] for y in range(world.world_map_size_y)] for x in range(world.world_map_size_x)]

    for x in range(world.world_map_size_x):
        for y in range(world.world_map_size_y):
            for z in range(world.world_map_size_z):
                scene[x][y][z] = world.get_location(x, y, z).description

    for x in range(world.world_map_size_x):
        for y in range(world.world_map_size_y):
            for z in range(world.world_map_size_z):
                print(scene[x][y][z], end="")
            print("")
    print("")


def run(descriptions):
    """Draws the scene of the described map. Public entry point of this unit."""
    render_scene(World(descriptions))
