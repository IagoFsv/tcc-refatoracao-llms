import skimage
import numpy as np


class Image:
    def __init__(self, array):
        self.image = array


class RGB_Image(Image):
    def draw_line(self, line_params):
        line = skimage.draw.line(line_params.y0, line_params.x0, line_params.y1, line_params.x1)
        self.image[line] = line_params.color
        return self


class LineParams:
    def __init__(self, y0, x0, y1, x1, color=(0, 0, 0)):
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1
        self.color = color


def executar(tamanho, segmento, cor=None):
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = segmento
    if cor is None:
        resultado = imagem.draw_line(LineParams(y0, x0, y1, x1))
    else:
        resultado = imagem.draw_line(LineParams(y0, x0, y1, x1, cor))
    return resultado.image
