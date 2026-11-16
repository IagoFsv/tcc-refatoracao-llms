class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Corners:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

class Values:
    def __init__(self, z11, z12, z21, z22):
        self.z11 = z11
        self.z12 = z12
        self.z21 = z21
        self.z22 = z22

def bilinear_interpolation(point, corners, values):
    x, y = point.x, point.y
    x1, x2, y1, y2 = corners.x1, corners.x2, corners.y1, corners.y2
    z11, z12, z21, z22 = values.z11, values.z12, values.z21, values.z22

    return  (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))

def executar(point, corners, values):
    return bilinear_interpolation(point, corners, values)
