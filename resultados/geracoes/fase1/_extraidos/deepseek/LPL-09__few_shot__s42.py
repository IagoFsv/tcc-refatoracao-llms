"""Desenho de um segmento numa imagem em tons de cinza.

Ponto de entrada publico: executar(parametros). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.

A imagem comeca toda em zero; o segmento e marcado com 1.
"""

import skimage
import numpy as np


class Parametros:
    """
    A class to represent the parameters.
    """

    def  __init__(self, linhas, colunas, y0, x0, y1, x1):
        """
        Create a Parameters object.

        @param linhas: number of rows
        @param colunas: number of columns
        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        """
        self.linhas = linhas
        self.colunas = colunas
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1


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

    def draw_line(self, y0, x0, y1, x1):
        """
        Draw a line on the image.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        @return: image with line drawn on it
        """
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = 1
        return self


def executar(parametros: Parametros):
    """parametros: uma instancia da classe Parametros."""
    imagem = Image(np.zeros((parametros.linhas, parametros.colunas)))
    resultado = imagem.draw_line(parametros.y0, parametros.x0, parametros.y1, parametros.x1)
    return resultado.image
