from dataclasses import dataclass

@dataclass
class Interpolacao:
    x: float
    y: float
    x1: float
    x2: float
    y1: float
    y2: float
    z11: float
    z12: float
    z21: float
    z22: float

def bilinear_interpolation(interpolacao: Interpolacao):
    x, y, x1, x2, y1, y2, z11, z12, z21, z22 = interpolacao
    return  (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))


def executar(ponto, cantos, valores):
    interpolacao = Interpolacao(*ponto, *cantos, *valores)
    return bilinear_interpolation(interpolacao)
