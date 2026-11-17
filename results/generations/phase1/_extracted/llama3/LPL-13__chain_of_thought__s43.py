class BilinearInterpolationParams:
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

def bilinear_interpolation(params: BilinearInterpolationParams) -> float:
    x = params.x
    y = params.y
    x1 = params.x1
    x2 = params.x2
    y1 = params.y1
    y2 = params.y2
    z11 = params.z11
    z12 = params.z12
    z21 = params.z21
    z22 = params.z22
    return (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))

def run(point, corners, values):
    """point: (x, y). corners: (x1, x2, y1, y2). values: (z11, z12, z21, z22). Public entry point of this unit."""
    params = BilinearInterpolationParams(*point, *corners, *values)
    return bilinear_interpolation(params)
