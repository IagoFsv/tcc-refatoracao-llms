class Point:
    def __init__(self, x, y, x1, x2, y1, y2, z11, z12, z21, z22):
        self.x = x
        self.y = y
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z11 = z11
        self.z12 = z12
        self.z21 = z21
        self.z22 = z22

def bilinear_interpolation(point: Point) -> float:
    x, y = point.x, point.y
    x1, x2, y1, y2 = point.x1, point.x2, point.y1, point.y2
    z11, z12, z21, z22 = point.z11, point.z12, point.z21, point.z22
    return (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))

def executar(ponto, cantos, valores):
    point = Point(*ponto, *canto(*canto), *valores)
    return bilinear_interpolation(point)
