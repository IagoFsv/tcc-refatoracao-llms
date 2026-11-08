import skimage
import numpy as np


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

    def draw_line(self, y0, x0, y1, x1, color=(0, 0, 0)):
        """
        Draw a line on the image.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        @param color: color of the line
        @return: image with line drawn on it
        """
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = color
        return self


class DrawSegment:
    def __init__(self, tamanho, segmento, cor=None):
        self.tamanho = tamanho
        self.segmento = segmento
        self.cor = cor if cor is not None else (0, 0, 0)


def executar(draw_segment: DrawSegment):
    """tamanho: (linhas, colunas). segmento: (y0, x0, y1, x1). cor: (r, g, b)."""
    imagem = RGB_Image(np.full((*draw_segment.tamanho, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = draw_segment.segmento
    resultado = imagem.draw_line(y0, x0, y1, x1, draw_segment.cor)
    return resultado.image
