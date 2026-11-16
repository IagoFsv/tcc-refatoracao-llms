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

    def draw_circle(self, center, radius, color=(0, 0, 0)):
        """
        Draw a circle on the image.

        @param center: tuple (x, y) representing the center of the circle
        @param radius: radius of the circle
        @param color: color of the circle
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk(center, radius, shape=self.image.shape)
        self.image[circle] = color
        return self


class DrawingParameters:
    def __init__(self, tamanho, disco, cor=None):
        self.tamanho = tamanho
        self.disco = disco
        self.cor = cor if cor is not None else (0, 0, 0)


def executar(drawing_params):
    """tamanho: (linhas, colunas). disco: (x, y, raio). cor: (r, g, b)."""
    imagem = RGB_Image(np.full(drawing_params.tamanho + (3,), 255, dtype=np.uint8))
    x, y, raio = drawing_params.disco
    resultado = imagem.draw_circle((x, y), raio, drawing_params.cor)
    return resultado.image
