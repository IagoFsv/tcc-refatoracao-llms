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


class Line:
    """
    A class to represent a line.
    """

    def __init__(self, y0, x0, y1, x1, color=(0, 0, 0)):
        """
        Create a Line object.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        @param color: color of the line
        """
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1
        self.color = color


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    def draw_line(self, line):
        """
        Draw a line on the image.

        @param line: Line object
        @return: image with line drawn on it
        """
        line_object = skimage.draw.line(line.y0, line.x0, line.y1, line.x1)
        self.image[line_object] = line.color
        return self


def executar(tamanho, segmento, cor=None):
    """tamanho: (linhas, colunas). segmento:  (y0, x0, y1, x1). cor: (r, g, b)."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = segmento
    if cor is None:
        line = Line(y0, x0, y1, x1)
    else:
        line = Line(y0, x0, y1, x1, cor)
    resultado = imagem.draw_line(line)
    return resultado.image
