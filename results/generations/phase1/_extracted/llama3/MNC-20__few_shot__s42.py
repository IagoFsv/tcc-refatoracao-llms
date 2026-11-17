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


class Plane:
    """A two-dimensional map cell, with the descriptions on the z-axis.

    The size on each axis comes from the first element; if the rows have
    different sizes, the map is irregular.
    """

    def __init__(self, plane):
        self.plane_map = [[Location(text) for text in row] for row in plane]
        self.plane_map_size_y = len(plane)
        self.plane_map_size_z = len(plane[0])

    def get_location(self, y, z):
        return self.plane_map[y][z]


class World:
    """Map built from the descriptions: descriptions[x][y][z].

    The size on each axis comes from the first element; if the rows have
    different sizes, the map is irregular.
    """

    def __init__(self, descriptions):
        self.world_map = [Plane(plane) for plane in descriptions]
        self.world_map_size_x = len(descriptions)

    def get_plane(self, x):
        return self.world_map[x]

    def get_location(self, x, y, z):
        plane = self.get_plane(x)
        return plane.get_location(y, z)


def render_scene(world):
    """Render the current scene."""
    print("\n" * 100)


    # Print out the world map
    for x in range(world.world_map_size_x):
        for y in range(len(world.get_plane(x).plane_map)):
            for z in range(len(world.get_plane(x).plane_map[y])):
                print(world.get_plane(x).get_location(y, z).get_description(), end="")
            print("")
    print("")


def run(descriptions):
    """Draws the scene of the described map. Public entry point of this unit."""
    render_scene(World(descriptions))
