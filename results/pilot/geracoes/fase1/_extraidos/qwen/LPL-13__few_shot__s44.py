from dataclasses import dataclass, asdict

@dataclass
class Ponto:
    x: float
    y: float

@dataclass
class Retangulo:
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

def bilinear_interpolation(ponto: Ponto, retangulo: Retangulo, valores: Valores):
    x, y = ponto.x, ponto.y
    x1, x2, y1, y2 = retangulo.x1, retangulo.x2, retangulo.y1, retangulo.y2
    z11, z12, z21, z22 = valores.z11, valores.z12, valores.z21, valores.z22
    return (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))

def executar(ponto: Ponto, retangulo: Retangulo, valores: Valores):
    return bilinear_interpolation(ponto, retangulo, valores)
