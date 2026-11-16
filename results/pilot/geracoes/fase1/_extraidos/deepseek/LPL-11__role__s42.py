"""Desenho de um disco colorido numa imagem RGB.

Ponto de entrada publico: executar(tamanho, disco, cor=None). Nao altere o
nome nem a assinatura dessa funcao; o restante do arquivo pode ser
reorganizado livremente.

A imagem comeca toda branca (255 nos tres canais). Sem cor, vale a cor
padrao do desenho. O disco e recortado na borda da imagem.
"""

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

        
        @param circle_params: parameters for the circle: x, y, radius, color
        @return: image with circle drawn on it
        """
        x, y, radius, color = circle_params.x, circle_params.y, circle_params.radius, circle_params.color
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = color
        return self


class CircleParams:
    """
    Class to represent the parameters of a circle.
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
        cor = (0, 0, 0)
    circle_params = CircleParams(x, y, raio, cor)
    resultado = imagem.draw_circle(circle_params)
    return resultado.image
