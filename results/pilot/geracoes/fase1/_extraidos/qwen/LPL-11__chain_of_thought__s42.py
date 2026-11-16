import skimage
import numpy as np

class DrawingParameters:
    def __init__(self, tamanho, disco, cor=None):
        self.tamanho = tamanho
        self.disco = disco
        self.cor = cor

class Image:
    def __init__(self, array):
        self.image = array

class RGB_Image(Image):
    def draw_circle(self, x, y, radius, color=(0, 0, 0)):
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = color
        return self

def executar(drawing_params):
    tamanho = drawing_params.tamanho
    disco = drawing_params.disco
    cor = drawing_params.cor
    
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    x, y, raio = disco
    if cor is None:
        resultado = imagem.draw_circle(x, y, raio)
    else:
        resultado = imagem.draw_circle(x, y, raio, cor)
    return resultado.image
