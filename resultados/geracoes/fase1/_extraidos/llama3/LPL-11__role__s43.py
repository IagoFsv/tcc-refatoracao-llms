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

    def draw_circle(self, circle_properties):
        """
        Draw a circle on the image.

        @param circle_properties: Object containing circle properties
        @return: image with circle drawn on it
        """
        circle_properties = circle_properties._asdict()
        x, y, radius = circle_properties['center'], circle_properties['radius'], circle_properties['radius']
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = circle_properties['color']
        return self


class CircleProperties:
    """
    Class to represent circle properties.
    """

    def __init__(self, center, radius, color):
        """
        Create a CircleProperties object.

        @param center: (x, y) coordinates of the center
        @param radius: radius of the circle
        @param color: color of the circle
        """
        self.center = center
        self.radius = radius
        self.color = color


def executar(tamanho, disco):
    """tamanho: (linhas, colunas). disco: (center, radius)."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    circle_properties = CircleProperties(disco, disco[2], (0, 0, 0))
    resultado = imagem.draw_circle(circle_properties)
    return resultado.image
