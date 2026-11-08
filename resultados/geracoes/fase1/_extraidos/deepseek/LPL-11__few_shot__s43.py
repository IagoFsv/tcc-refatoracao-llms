import skimage
import numpy as np
from dataclasses import dataclass, asdict

@dataclass
class Circulo:
    x: int
    y: int
    raio: int
    cor: tuple = (0, 0, 0)

class Image:
    """
    A class to represent an image.
    """

    def __init__(self, array):
        """
        Create an Image object from a numpy array.

        @param array: numpy array representing the image
        """
        self.image = array


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    def draw_circle(self, circulo: Circulo):
        """
        Draw a circle on the image.

        @param circulo: Circulo object representing the circle to be drawn
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk((circulo.y, circulo.x), circulo.raio, shape=self.image.shape)
        self.image[circle] = circulo.cor
        return self


def executar(tamanho, disco, cor=None):
    """tamanho: (linhas, colunas). disco: (x, y, raio). cor: (r, g, b)."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    x, y, raio = disco
    if cor is None:
        circulo = Circulo(x, y, raio)
    else:
        circulo = Circulo(x, y, raio, cor)
    resultado = imagem.draw_circle(circulo)
    return resultado.image
