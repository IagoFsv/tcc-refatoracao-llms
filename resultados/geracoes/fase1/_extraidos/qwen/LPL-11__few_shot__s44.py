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


class CircleParameters:
    def __init__(self, x, y, radius, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color


def executar(tamanho, disco_params, cor=None):
    """tamanho: (linhas, colunas). disco_params: CircleParameters. cor: (r, g, b)."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    if cor is None:
        resultado = imagem.draw_circle(disco_params.x, disco_params.y, disco_params.radius, disco_params.color)
    else:
        resultado = imagem.draw_circle(disco_params.x, disco_params.y, disco_params.radius, cor)
    return resultado.image
