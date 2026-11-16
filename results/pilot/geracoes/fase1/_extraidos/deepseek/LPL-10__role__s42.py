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

    def  __init__(self, array):
        """
        Create an Image object from a numpy array.

         @param array: numpy array representing the image
        """
        self.image = array


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    def draw_line(self, line_params):
        """
        Draw a line on the image.

        @param line_params: parameters of the line to be drawn
        @return: image with line drawn on it
        """
        line = skimage.draw.line(*line_params)
        self.image[line] = line_params[-1]
        return self


def executar(tamanho, segmento, cor=None):
    """tamanho: (linhas, colunas). segmento: (y0, x0, y1, x1). cor: (r, g, b)."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    resultado = imagem.draw_line(segmento + (cor if cor else (0, 0, 0)))
    return resultado.image
