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

    def draw_line(self, coordinates):
        """
        Draw a line on the image.

        @param coordinates: Coordinates of the line (y0, x0, y1, x1)
        @return: image with line drawn on it
        """
        y0, x0, y1, x1 = coordinates
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = 1
        return self


class Segment:
    """
    A class to represent a segment.
    """

    def __init__(self, y0, x0, y1, x1):
        """
        Create a Segment object from its coordinates.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        """
        self.coordinates = (y0, x0, y1, x1)


def executar(tamanho, segmento):
    """tamanho: (linhas, colunas). segmento: Segment object."""
    imagem = Image(np.zeros(tamanho))
    imagem.draw_line(segmento.coordinates)
    return imagem.image
