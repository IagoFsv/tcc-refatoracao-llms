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

    def draw_line(self, drawing_params):
        """
        Draw a line on the image.

        @param drawing_params: DrawingParams object
        @return: image with line drawn on it
        """
        y0, x0, y1, x1, color = drawing_params
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = color
        return self


class DrawingParams:
    """
    A class to represent drawing parameters.
    """

    def __init__(self, y0, x0, y1, x1, color=(0, 0, 0)):
        """
        Create a DrawingParams object.

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
    drawing_params = DrawingParams(*segmento)
    if drawing_params.color is None:
        resultado = imagem.draw_line(drawing_params)
    else:
        resultado = imagem.draw_line(drawing_params)
    return resultado.image
