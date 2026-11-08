from dataclasses import dataclass

@dataclass
class BilinearInterpolationData:
    x1: float
    x2: float
    y1: float
    y2: float
    z11: float
    z12: float
    z21: float
    z22: float

def bilinear_interpolation(data: BilinearInterpolationData, x: float, y: float) -> float:
    return (
        data.z11 * (data.x2 - x) * (data.y2 - y)
        + data.z21 * (x - data.x1) * (data.y2 - y)
        + data.z12 * (data.x2 - x) * (y - data.y1)
        + data.z22 * (x - data.x1) * (y - data.y1)
    ) / ((data.x2 - data.x1) * (data.y2 - data.y1))

def executar(ponto, cantos, valores):
    data = BilinearInterpolationData(*cants, *valores)
    x, y = ponto
    return bilinear_interpolation(data, x, y)
