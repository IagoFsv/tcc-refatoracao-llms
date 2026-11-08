import skimage
import numpy as np

class DrawingParameters:
    def __init__(self, tamanho, segmento, cor=None):
        self.tamanho = tamanho
        self.segmento = segmento
        self.cor = cor

class Image:
    def __init__(self, array):
        self.image = array

class RGB_Image(Image):
    def draw_line(self, y0, x0, y1, x1, color=(0, 0, 0)):
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = color
        return self

def executar(drawing_params):
    tamanho = drawing_params.tamanho
    segmento = drawing_params.segmento
    cor = drawing_params.cor
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = segmento
    if cor is None:
        resultado = imagem.draw_line(y0, x0, y1, x1)
    else:
        resultado = imagem.draw_line(y0, x0, y1, x1, cor)
    return resultado.image
