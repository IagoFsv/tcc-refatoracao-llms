class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Location:
    def __init__(self, coordinate):
        self.coordinate = coordinate

class WorldMap:
    def __init__(self, size_x, size_y, size_z):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.generate_world_map()

    def generate_world_map(self):
        self.map = [None] * self.size_x
        for i in range(self.size_x):
            self.map[i] = [None] * self.size_y
            for j in range(self.size_y):
                self.map[i][j] = [None] * self.size_z
                for k in range(self.size_z):
                    self.map[i][j][k] = Location(Coordinate(i, j, k))

    def get_location(self, x, y, z):
        return self.map[x][y][z].coordinate

def executar(x, y, z):
    return WorldMap(2, 3, 4).get_location(x, y, z)
