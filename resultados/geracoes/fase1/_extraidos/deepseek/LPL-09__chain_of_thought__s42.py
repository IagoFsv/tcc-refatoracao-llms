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

    def draw_line(self, line_params):
        """
        Draw a line on the image.

        @param line_params: object containing line parameters
        @return: image with line drawn on it
        """
        y0, x0, y1, x1 = line_params
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = 1
        return self


class LineParams:
    """
    A class to represent line parameters.
    """

    def __init__(self, y0, x0, y1, x1):
        """
        Create a LineParams object.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        """
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1


def executar(tamanho, segmento):
    """tamanho: (linhas, colunas). segmento: (y0, x0, y1, x1)."""
    imagem = Image(np.zeros(tamanho))
    line_params = LineParams(*segmento)
    resultado = imagem.draw_line(line_params)
    return resultado.image
