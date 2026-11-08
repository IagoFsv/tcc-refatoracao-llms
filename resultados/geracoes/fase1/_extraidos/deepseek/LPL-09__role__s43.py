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

    def draw_line(self, line_coordinates):
        """
        Draw a line on the image.

        @param line_coordinates: a dictionary with y0, x0, y1, x1 as keys
        @return: image with line drawn on it
        """
        y0, x0, y1, x1 = line_coordinates.values()
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = 1
        return self


def executar(tamanho, segmento):
    """tamanho: (linhas, colunas). segmento: (y0, x0, y1, x1)."""
    imagem = Image(np.zeros(tamanho))
    resultado = imagem.draw_line(segmento)
    return resultado.image
