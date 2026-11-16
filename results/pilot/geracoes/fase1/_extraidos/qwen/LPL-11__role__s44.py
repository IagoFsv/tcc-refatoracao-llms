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

    def draw_circle(self, position, radius, color=(0, 0, 0)):
        """
        Draw a circle on the image.

        @param position: (x, y) coordinates of the center
        @param radius: radius of the circle
        @param color: color of the circle
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk(position, radius, shape=self.image.shape)
        self.image[circle] = color
        return self


def draw_circle_params(position, radius, color):
    """
    Helper function to create a parameter object for drawing a circle.

    @param position: (x, y) coordinates of the center
    @param radius: radius of the circle
    @param color: color of the circle
    @return: dictionary containing the circle parameters
    """
    return {
        'x': position[0],
        'y': position[1],
        'radius': radius,
        'color': color
    }


def executar(tamanho, disco, cor=None):
    """tamanho: (linhas, colunas). disco: (x, y, raio). cor: (r, g, b)."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    circle_params = draw_circle_params(disco[:2], disco[2], cor or (0, 0, 0))
    resultado = imagem.draw_circle((circle_params['x'], circle_params['y']), circle_params['radius'], circle_params['color'])
    return resultado.image
