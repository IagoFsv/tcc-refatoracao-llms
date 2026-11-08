"""Desenho de um segmento numa imagem em tons de cinza.

Ponto de entrada publico: executar(tamanho, segmento). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.

A imagem comeca toda em zero; o segmento e marcado com 1.
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

    def draw_line(self, line_coordinates):
        """
        Draw a line on the image.

         @param line_coordinates: coordinates of the line to be drawn
         @return: image with line drawn on it
        """
        line = skimage.draw.line(line_coordinates.y0, line_coordinates.x0, line_coordinates.y1, line_coordinates.x1)
        self.image[line] = 1
        return self


class LineCoordinates:
    """
    A class to represent the coordinates of a line.
    """

    def __init__(self, y0, x0, y1, x1):
        """
        Create a LineCoordinates object.

         @param y0: y coordinate of the first point
         @param x0: x coordinate of the first point
         @param y1: y coordinate of the second point
         @param x1: x coordinate of the second point
        """
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1


def executar(tamanho, segmento):
    """tamanho:  (linhas, colunas). segmento: (y0, x0, y1, x1)."""
    imagem = Image(np.zeros(tamanho))
    line_coordinates = LineCoordinates(*segmento)
    resultado = imagem.draw_line(line_coordinates)
    return resultado.image
