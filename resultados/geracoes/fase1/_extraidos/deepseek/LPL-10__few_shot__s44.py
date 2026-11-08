import skimage
import numpy as np


class Image:
    def __init__(self, array):
        self.image = array


class RGB_Image(Image):
    def draw_line(self, line_params: tuple, color=(0, 0, 0)):
        line = skimage.draw.line(*line_params)
        self.image[line] = color
        return self


def executar(tamanho, segmento, cor=None):
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    if cor is None:
        resultado = imagem.draw_line(segmento)
    else:
        resultado = imagem.draw_line(segmento, cor)
    return resultado.image
