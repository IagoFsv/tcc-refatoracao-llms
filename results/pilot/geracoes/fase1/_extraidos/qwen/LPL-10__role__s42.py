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


class DrawLineParameters:
    def __init__(self, y0, x0, y1, x1, color=(0, 0, 0)):
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1
        self.color = color


def executar(tamanho, segmento_params, cor=None):
    """tamanho: (linhas, colunas). segmento_params: DrawLineParameters. cor: (r, g, b)."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    if cor is None:
        resultado = imagem.draw_line((segmento_params.y0, segmento_params.x0, segmento_params.y1, segmento_params.x1))
    else:
        segmento_params.color = cor
        resultado = imagem.draw_line((segmento_params.y0, segmento_params.x0, segmento_params.y1, segmento_params.x1))
    return resultado.image
