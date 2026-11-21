class Location:
    """A map cell, identified by its coordinates."""

    def  __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.location = (x, y, z)


class World:
    def  __init__(self, size_x, size_y, size_z):
        self.world_map_size_x = size_x
        self.world_map_size_y = size_y
        self.world_map_size_z = size_z
        self.world_map_size = self.world_map_size_x * self.world_map_size_y * self.world_map_size_z
        self.generate_world_map()

    def generate_world_map(self):
        self.world_map = []
        for x in range(self.world_map_size_x):
            plane = []
            for y in range(self.world_map_size_y):
                row = []
                for z in range(self.world_map_size_z):
                    row.append(Location(x, y, z))
                plane.append(row)
            self.world_map.append(plane)


def run(size_x, size_y, size_z):
    """Builds a map of the given size and returns the coordinates of each cell,
    grouped by x and then by y. Public entry point of this unit."""
    world = World(size_x, size_y, size_z)
    planes = []
    for plane in world.world_map:
        rows = []
        for row in plane:
            rows.append([cell.location for cell in row])
        planes.append(rows)
    return planes
