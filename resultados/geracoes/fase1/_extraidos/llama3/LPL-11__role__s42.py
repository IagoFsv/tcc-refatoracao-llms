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

        @param circle_params: CircleParams object
        @return: image with circle drawn on it
        """
        x, y, radius = circle_params.x, circle_params.y, circle_params.radius
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = circle_params.color
        return self


class CircleParams:
    """
    A class to represent circle parameters.
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


def executar(tamanho, disco):
    """tamanho: (linhas, colunas). disco: CircleParams object."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    if cor is None:
        resultado = imagem.draw_circle(disco)
    else:
        resultado = imagem.draw_circle(disco)
    return resultado.image
