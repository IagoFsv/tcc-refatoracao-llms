from dataclasses import dataclass, asdict

@dataclass
class Ponto:
    x: float
    y: float

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

def bilinear_interpolation(ponto: Ponto, cantos: Cantos, valores: Valores):
    """Bilinear interpolation. It considers the values of the four points
    around the point to be interpolated and returns the interpolated value.
    Made with a lot of help from GitHub Copilot.

    Parameters
    ----------
    ponto : Ponto
        Ponto de entrada para a interpolação.
    cantos : Cantos
        Coordenadas dos cantos do retângulo.
    valores : Valores
        Valores dos pontos nos cantos do retângulo.

    Returns
    -------
    float
        Valor interpolado.

    Examples
    --------
    >>> from rocketpy.tools import bilinear_interpolation
    >>> bilinear_interpolation(Ponto(0.5, 0.5), Cantos(0, 1, 0, 1), Valores(0, 1, 1, 0))
    0.5
    """
    x, y = ponto.x, ponto.y
    x1, x2, y1, y2 = cantos.x1, cantos.x2, cantos.y1, cantos.y2
    z11, z12, z21, z22 = valores.z11, valores.z12, valores.z21, valores.z22
    return (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))

def executar(ponto: Ponto, cantos: Cantos, valores: Valores):
    """Executa a interpolação bilinear."""
    return bilinear_interpolation(ponto, cantos, valores)
