from dataclasses import dataclass, asdict

@dataclass
class InterpolationData:
    ponto: tuple
    cantos: tuple
    valores: tuple

def bilinear_interpolation(data: InterpolationData):
    x, y = data.ponto
    x1, x2, y1, y2 = data.cantos
    z11, z12, z21, z22 = data.valores
    return (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))

def executar(data: InterpolationData):
    return bilinear_interpolation(data)
