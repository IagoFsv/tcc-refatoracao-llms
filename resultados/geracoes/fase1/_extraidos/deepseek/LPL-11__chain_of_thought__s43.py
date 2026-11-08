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

    def draw_circle(self, circle):
        """
        Draw a circle on the image.

        @param circle: Circle object
        @return: image with circle drawn on it
        """
        circle_coords = skimage.draw.disk((circle.y, circle.x), circle.radius, shape=self.image.shape)
        self.image[circle_coords] = circle.color
        return self


class Circle:
    """
    Circle class to store parameters of draw_circle method.
    """

    def __init__(self, x, y, radius, color=(0, 0, 0)):
        """
        Create a Circle object.

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
        circle = Circle(x, y, raio)
    else:
        circle = Circle(x, y, raio, cor)
    resultado = imagem.draw_circle(circle)
    return resultado.image
