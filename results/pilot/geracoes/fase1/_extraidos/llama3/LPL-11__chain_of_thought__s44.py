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


class Circle:
    """
    A class to represent a circle.
    """

    def __init__(self, x, y, radius):
        """
        Create a Circle object.

        @param x: x coordinate of the center
        @param y: y coordinate of the center
        @param radius: radius of the circle
        """
        self.x = x
        self.y = y
        self.radius = radius


class Color:
    """
    A class to represent a color.
    """

    def __init__(self, r, g, b):
        """
        Create a Color object.

        @param r: red component of the color
        @param g: green component of the color
        @param b: blue component of the color
        """
        self.r = r
        self.g = g
        self.b = b


def executar(tamanho, circle, color=None):
    """tamanho: (linhas, colunas). circle: Circle object. color: Color object or None."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    if color is None:
        resultado = imagem.draw_circle(circle.x, circle.y, circle.radius)
    else:
        resultado = imagem.draw_circle(circle.x, circle.y, circle.radius, (color.r, color.g, color.b))
    return resultado.image
