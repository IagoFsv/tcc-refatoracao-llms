import skimage
import numpy as np


class Image:
    def __init__(self, array):
        self.image = array


class RGB_Image(Image):
    def draw_line(self, line):
        line_object = skimage.draw.line(line.y0, line.x0, line.y1, line.x1)
        self.image[line_object] = line.color if line.color else (0, 0, 0)
        return self


class Line:
    def __init__(self, y0, x0, y1, x1, color=None):
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1
        self.color = color if color else (0, 0, 0)


def executar(tamanho, segmento, cor=None):
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = segmento
    line = Line(y0, x0, y1, x1, cor)
    resultado = imagem.draw_line(line)
    return resultado.image
