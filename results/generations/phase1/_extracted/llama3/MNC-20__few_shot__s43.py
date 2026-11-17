class Location:
    """A map cell, with the description that appears in the scene."""

    def __init__(self, description):
        self.description = description

    def get_description(self):
        return self.description


class Plane:
    """A map plane, with its own set of locations."""

    def __init__(self, locations):
        self.locations = locations

    def get_location(self, z):
        return self.locations[z]


class World:
    """Map built from the descriptions: descriptions[x][y][z].

    The size on each axis comes from the first element; if the rows have
    different sizes, the map is irregular.
    """

    def __init__(self, descriptions):
        self.world_map = []
        first_plane = descriptions[0]
        self.world_map_size_x = len(descriptions)
        self.world_map_size_y = len(first_plane)
        for plane in descriptions:
            self.world_map.append(Plane([Location(text) for text in plane]))
        self.world_map_size_z = len(first_plane[0])

    def get_location(self, x, y, z):
        return self.world_map[x].locations[y].locations[z]


def render_scene(world):
    """Render the current scene."""
    print("\n" * 100)

    # Print out the world map
    for x in range(world.world_map_size_x):
        for y in range(world.world_map_size_y):
            for z in range(world.world_map_size_z):
                print(world.get_location(x, y, z).get_description(), end="")
            print("")
    print()


def run(descriptions):
    """Draws the scene of the described map. Public entry point of this unit."""
    render_scene(World(descriptions))
