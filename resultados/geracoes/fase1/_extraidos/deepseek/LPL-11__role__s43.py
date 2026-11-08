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

    def draw_circle(self, circle_params):
        """
        Draw a circle on the image.

        @param circle_params: parameters for the circle drawing
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk(
            (circle_params.y, circle_params.x),
            circle_params.radius,
            shape=self.image.shape
        )
        self.image[circle] = circle_params.color
        return self


class CircleParams:
    """
    Class to represent parameters for circle drawing.
    """

    def __init__(self, x, y, radius, color=(0, 0, 0)):
        """
        Create a CircleParams object.

        @param x: x coordinate of the center
        @param y: y coordinate of the center
        @param radius: radius of the circle
        @param color: color of the circle
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color


def executar(tamanho, disco, cor=None):
    """tamanho: (linhas, colunas). disco: (x, y, raio). cor: (r, g, b)."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    x, y, raio = disco
    if cor is None:
        resultado = imagem.draw_circle(CircleParams(x, y, raio))
    else:
        resultado = imagem.draw_circle(CircleParams(x, y, raio, cor))
    return resultado.image
