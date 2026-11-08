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

    def draw_circle(self, x, y, radius, color=(0, 0, 0)):
        """
        Draw a circle on the image.

        @param x: x coordinate of the center
        @param y: y coordinate of the center
        @param radius: radius of the circle
        @param color: color of the circle
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = color
        return self


class DrawParameters:
    """
    Class to group drawing parameters together.
    """

    def __init__(self, tamanho, disco, cor=None):
        """
        Initialize the DrawParameters object.

        @param tamanho: tuple representing the size of the image (linhas, colunas)
        @param disco: tuple representing the circle (x, y, raio)
        @param cor: tuple representing the color (r, g, b)
        """
        self.tamanho = tamanho
        self.disco = disco
        self.cor = cor


def executar(draw_params):
    """tamanho: (linhas, colunas). disco: (x, y, raio). cor: (r, g, b)."""
    imagem = RGB_Image(np.full(draw_params.tamanho, 255, dtype=np.uint8))
    x, y, raio = draw_params.disco
    if draw_params.cor is None:
        resultado = imagem.draw_circle(x, y, raio)
    else:
        resultado = imagem.draw_circle(x, y, raio, draw_params.cor)
    return resultado.image
