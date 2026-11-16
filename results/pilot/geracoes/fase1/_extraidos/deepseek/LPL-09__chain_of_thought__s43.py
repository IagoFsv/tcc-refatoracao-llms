import skimage
import numpy as np

class Line:
    """
    A class to represent a line.
    """
    def __init__(self, y0, x0, y1, x1):
        """
        Create a Line object with two points.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        """
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1

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

    def draw_line(self, line):
        """
        Draw a line on the image.

        @param line: Line object representing the line to draw
        @return: image with line drawn on it
        """
        line = skimage.draw.line(line.y0, line.x0, line.y1, line.x1)
        self.image[line] = 1
        return self

def executar(tamanho, line):
    """
    tamanho: (linhas, colunas).
    line: Line object representing the line to draw.
    """
    image = Image(np.zeros(tamanho))
    resultado = image.draw_line(line)
    return resultado.image
