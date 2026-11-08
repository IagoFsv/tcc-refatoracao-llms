import skimage
import numpy as np


class Image:
    def __init__(self, array):
        self.image = array


class RGB_Image(Image):
    def draw_circle(self, center, radius, color=(0, 0, 0)):
        circle = skimage.draw.disk(center.coords, radius, shape=self.image.shape)
        self.image[circle] = color
        return self


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    @property
    def coords(self):
        return (self.y, self.x)


def executar(tamanho, disco, cor=None):
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    x, y, raio = disco
    circle = Circle(x, y, raio)
    if cor is None:
        resultado = imagem.draw_circle(circle, raio)
    else:
        resultado = imagem.draw_circle(circle, raio, cor)
    return resultado.image
