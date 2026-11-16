import skimage
import numpy as np


class Image:
    def __init__(self, array):
        self.image = array

    def draw_line(self, line_coordinates):
        line = skimage.draw.line(line_coordinates.y0, line_coordinates.x0, line_coordinates.y1, line_coordinates.x1)
        self.image[line] = 1
        return self


class LineCoordinates:
    def __init__(self, y0, x0, y1, x1):
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1


def executar(tamanho, segmento):
    imagem = Image(np.zeros(tamanho))
    line_coordinates = LineCoordinates(*segmento)
    resultado = imagem.draw_line(line_coordinates)
    return resultado.image
