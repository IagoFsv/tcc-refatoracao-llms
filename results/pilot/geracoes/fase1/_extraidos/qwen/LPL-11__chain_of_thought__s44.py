import skimage
import numpy as np

class Desenho:
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

def executar(desenho):
    """desenho: objeto do tipo Desenho."""
    imagem = RGB_Image(np.full(desenho.tamanho, 255, dtype=np.uint8))
    x, y, raio = desenho.disco
    if desenho.cor is None:
        resultado = imagem.draw_circle(x, y, raio)
    else:
        resultado = imagem.draw_circle(x, y, raio, desenho.cor)
    return resultado.image
