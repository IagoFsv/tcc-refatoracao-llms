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

    def draw_line(self, line, color=(0, 0, 0)):
        """
        Draw a line on the image.

        @param line: tuple of (y0, x0, y1, x1) coordinates of the line
        @param color: color of the line
        @return: image with line drawn on it
        """
        self.image[line] = color
        return self


class DrawParameters:
    def __init__(self, y0, x0, y1, x1, cor=None):
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1
        self.cor = cor


def executar(tamanho, segmento, cor=None):
    """tamanho: (linhas, colunas). segmento: (y0, x0, y1, x1). cor: (r, g, b)."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    params = DrawParameters(segmento[0], segmento[1], segmento[2], segmento[3], cor)
    y0, x0, y1, x1 = params.y0, params.x0, params.y1, params.x1
    if params.cor is None:
        resultado = imagem.draw_line((y0, x0, y1, x1))
    else:
        resultado = imagem.draw_line((y0, x0, y1, x1), params.cor)
    return resultado.image
