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
    """A 2D map cell, with a list of locations in the z-axis.

    Public interface: get_location(z) -> Location
    """

    def __init__(self, locations):
        self.locations = locations

    def get_location(self, z):
        return self.locations[z]


class World:
    """Map built from the descriptions: descriptions[x][y].

    The size on each axis comes from the first element; if the rows have
    different sizes, the map is irregular.
    """

    def __init__(self, descriptions):
        self.world_map = [[Plane(locations) for locations in plane] for plane in descriptions]
        self.world_map_size_x = len(descriptions)
        self.world_map_size_y = len(descriptions[0])

    def get_location(self, x, y, z):
        return self.world_map[x][y].get_location(z)


def render_scene(world):
    """Render the current scene."""
    print("\n" * 100)

    for x in range(world.world_map_size_x):
        for y in range(world.world_map_size_y):
            for z in range(len(world.world_map[x][y].locations)):
                print(world.get_location(x, y, z).get_description(), end="")
            print("")
    print()


def run(descriptions):
    """Draws the scene of the described map. Public entry point of this unit."""
    render_scene(World(descriptions))
