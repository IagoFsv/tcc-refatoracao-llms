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
    return (
        valores.z11 * (retangulo.x2 - ponto.x) * (retangulo.y2 - ponto.y)
        + valores.z21 * (ponto.x - retangulo.x1) * (retangulo.y2 - ponto.y)
        + valores.z12 * (retangulo.x2 - ponto.x) * (ponto.y - retangulo.y1)
        + valores.z22 * (ponto.x - retangulo.x1) * (ponto.y - retangulo.y1)
    ) / ((retangulo.x2 - retangulo.x1) * (retangulo.y2 - retangulo.y1))

def executar(ponto: Ponto, retangulo: Retangulo, valores: Valores):
    return bilinear_interpolation(ponto, retangulo, valores)
