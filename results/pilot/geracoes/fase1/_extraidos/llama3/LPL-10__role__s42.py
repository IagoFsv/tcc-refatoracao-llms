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

    def draw_line(self, parameters):
        """
        Draw a line on the image.

        @param parameters: LineDrawingParameters
        @return: image with line drawn on it
        """
        y0, x0, y1, x1, color = parameters
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = color
        return self


class LineDrawingParameters:
    """
    A class to hold parameters for drawing a line.
    """

    def __init__(self, y0, x0, y1, x1, color=None):
        """
        Create a LineDrawingParameters object.

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
    parameters = LineDrawingParameters(*segmento)
    if parameters.color is None:
        resultado = imagem.draw_line(parameters)
    else:
        resultado = imagem.draw_line(parameters)
    return resultado.image
