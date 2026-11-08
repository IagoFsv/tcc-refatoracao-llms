class InterpolationParameters:
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


def bilinear_interpolation(params):
    x, y = params.x, params.y
    x1, x2, y1, y2 = params.x1, params.x2, params.y1, params.y2
    z11, z12, z21, z22 = params.z11, params.z12, params.z21, params.z22

    return (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))


def executar(ponto, cantos, valores):
    params = InterpolationParameters(*ponto, *cantos, *valores)
    return bilinear_interpolation(params)
