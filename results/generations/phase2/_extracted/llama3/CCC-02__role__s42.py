"""Three-dimensional map of an adventure game: drawing the scene on the terminal.

Public entry point: run(descriptions). Do not change its name or signature;
the rest of the file may be freely reorganized.
"""


class Location:
    """A map cell, with the description that appears in the scene."""

    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class World:
    """Map built from the descriptions: descriptions[x][y][z].

    The size on each axis comes from the first element; if the rows have
    different sizes, the map is irregular.
    """

    def __init__(self, descriptions):
        self.world_map = []
        for plane in descriptions:
            rows = []
            for row in plane:
                rows.append([Location(text) for text in row])
            self.world_map.append(rows)
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
                scene[x][y][z] = world.get_location(x, y, z).get_description()

    for x in range(world.world_map_size_x):
        for y in range(world.world_map_size_y):
            for z in range(world.world_map_size_z):
                print(scene[x][y][z], end="")
            print("")
    print("")


def run(descriptions):
    """Draws the scene of the described map. Public entry point of this unit."""
    world = World(descriptions)
    for x in range(world.world_map_size_x):
        for y in range(world.world_map_size_y):
            for z in range(world.world_map_size_z):
                scene = world.get_location(x, y, z).get_description()
                print(scene, end="")
            print("")
    print("")
