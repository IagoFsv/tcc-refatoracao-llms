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

    def draw_line(self, params):
        """
        Draw a line on the image.

        @param params: LineParams object
        @return: image with line drawn on it
        """
        y0, x0, y1, x1, color = params
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = color
        return self


class LineParams:
    """
    A class to represent line parameters.
    """

    def __init__(self, y0, x0, y1, x1, color):
        """
        Create a LineParams object.

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


def executar(tamanho, segmento):
    """tamanho: (linhas, colunas). segmento: (y0, x0, y1, x1)."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = segmento
    params = LineParams(y0, x0, y1, x1, (0, 0, 0))
    resultado = imagem.draw_line(params)
    return resultado.image
