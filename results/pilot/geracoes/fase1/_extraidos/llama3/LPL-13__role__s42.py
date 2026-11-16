from dataclasses import dataclass

@dataclass
class Cantos:
    x1: float
    x2: float
    y1: float
    y2: float

@dataclass
class Valores:
    z11: float
    z12: float
    z21: float
    z22: float

def bilinear_interpolation(x: float, y: float, cantos: Cantos, valores: Valores) -> float:
    x1, x2, y1, y2 = cantos
    z11, z12, z21, z22 = valores
    return (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))

def executar(ponto: tuple, cantos: Cantos, valores: Valores) -> float:
    x, y = ponto
    return bilinear_interpolation(x, y, cantos, valores)
