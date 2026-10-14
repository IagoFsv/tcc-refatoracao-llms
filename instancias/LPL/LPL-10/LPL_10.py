"""Desenho de um segmento colorido numa imagem RGB.

Ponto de entrada publico: executar(tamanho, segmento, cor=None). Nao altere o
nome nem a assinatura dessa funcao; o restante do arquivo pode ser
reorganizado livremente.

A imagem comeca toda branca (255 nos tres canais). Sem cor, vale a cor
padrao do desenho.
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

    def draw_line(self, y0, x0, y1, x1, color=(0, 0, 0)):
        """
        Draw a line on the image.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        @param color: color of the line
        @return: image with line drawn on it
        """
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = color
        return self


def executar(tamanho, segmento, cor=None):
    """tamanho: (linhas, colunas). segmento: (y0, x0, y1, x1). cor: (r, g, b)."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = segmento
    if cor is None:
        resultado = imagem.draw_line(y0, x0, y1, x1)
    else:
        resultado = imagem.draw_line(y0, x0, y1, x1, cor)
    return resultado.image
