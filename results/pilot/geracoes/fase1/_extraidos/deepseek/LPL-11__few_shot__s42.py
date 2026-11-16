"""Desenho de um disco colorido numa imagem RGB.

Ponto de entrada publico: executar(parametros_imagem, disco, cor=None). Nao altere o
nome nem a assinatura dessa funcao; o restante do arquivo pode ser
reorganizado livremente.

A imagem comeca toda branca  (255 nos tres canais). Sem cor, vale a cor
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

    def draw_circle(self, parametros_imagem, disco, cor=(0, 0, 0)):
        """
        Draw a circle on the image.

         @param parametros_imagem: (linhas, colunas)
         @param disco: (x, y, raio)
         @param cor: (r, g, b)
         @return: image with circle drawn on it
        """
        circle = skimage.draw.disk((disco[1], disco[0]), disco[2], shape=parametros_imagem)
        self.image[circle] = cor
        return self


def executar(parametros_imagem, disco, cor=None):
    """parametros_imagem: (linhas, colunas). disco: (x, y, raio). cor: (r, g, b)."""
    imagem = RGB_Image(np.full((*parametros_imagem, 3), 255, dtype=np.uint8))
    if cor is None:
        resultado = imagem.draw_circle(parametros_imagem, disco)
    else:
        resultado = imagem.draw_circle(parametros_imagem, disco, cor)
    return resultado.image
