import skimage
import numpy as np
from dataclasses import dataclass, asdict

@dataclass
class Segmento:
    y0: int
    x0: int
    y1: int
    x1: int

@dataclass
class Tamanho:
    linhas: int
    colunas: int

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

    def draw_line(self, segmento: Segmento):
        """
        Draw a line on the image.

        @param segmento: Segmento object representing the line
        @return: image with line drawn on it
        """
        line = skimage.draw.line(segmento.y0, segmento.x0, segmento.y1, segmento.x1)
        self.image[line] = 1
        return self


def executar(tamanho: Tamanho, segmento: Segmento):
    """tamanho: Tamanho(linhas, colunas). segmento: Segmento(y0, x0, y1, x1)."""
    imagem = Image(np.zeros((tamanho.linhas, tamanho.colunas)))
    resultado = imagem.draw_line(segmento)
    return resultado.image
