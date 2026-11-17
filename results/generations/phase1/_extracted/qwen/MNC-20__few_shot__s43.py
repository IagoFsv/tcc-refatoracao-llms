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
    """A 2D plane in the map, built from a list of rows."""

    def __init__(self, rows):
        self.rows = rows
        self.size_y = len(rows)
        self.size_z = len(rows[0]) if rows else 0

    def get_location(self, y, z):
        return self.rows[y][z]


class World:
    """Map built from the descriptions: descriptions[x][y][z].

    The size on each axis comes from the first element; if the rows have
    different sizes, the map is irregular.
    """

    def __init__(self, descriptions):
        self.planes = [Plane(plane) for plane in descriptions]
        self.size_x = len(descriptions)
        self.size_y = self.planes[0].size_y if self.planes else 0
        self.size_z = self.planes[0].size_z if self.planes else 0

    def get_location(self, x, y, z):
        return self.planes[x].get_location(y, z)


def render_scene(world):
    """Render the current scene."""
    print("\n" * 100)

    # Print out the world map
    scene = [[["" for z in range(world.size_z)] for y in range(world.size_y)] for x in range(world.size_x)]

    for x in range(world.size_x):
        for y in range(world.size_y):
            for z in range(world.size_z):
                scene[x][y][z] = world.get_location(x, y, z).get_description()

    for x in range(world.size_x):
        for y in range(world.size_y):
            for z in range(world.size_z):
                print(scene[x][y][z], end="")
            print("")
    print("")


def run(descriptions):
    """Draws the scene of the described map. Public entry point of this unit."""
    render_scene(World(descriptions))
