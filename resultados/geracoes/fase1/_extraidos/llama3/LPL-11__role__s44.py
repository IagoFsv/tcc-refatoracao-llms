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

        @param circle_params: CircleParams object with x, y, radius, and color
        @return: image with circle drawn on it
        """
        x, y, radius, color = circle_params
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = color
        return self


class CircleParams:
    """
    A class to represent circle parameters.
    """

    def __init__(self, x, y, radius, color):
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


def executar(tamanho, disco_params):
    """tamanho: (linhas, colunas). disco_params: CircleParams object."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    if disco_params.color is None:
        resultado = imagem.draw_circle((disco_params.x, disco_params.y, disco_params.radius))
    else:
        resultado = imagem.draw_circle((disco_params.x, disco_params.y, disco_params.radius, disco_params.color))
    return resultado.image
