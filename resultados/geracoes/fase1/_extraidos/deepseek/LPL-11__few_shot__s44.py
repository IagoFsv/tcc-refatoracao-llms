import skimage
import numpy as np


class Image:
    def __init__(self, array):
        self.image = array


class RGB_Image(Image):
    def draw_circle(self, center, radius, color=(0, 0, 0)):
        circle = skimage.draw.disk(center, radius, shape=self.image.shape)
        self.image[circle] = color
        return self


class Circle:
    def __init__(self, x, y, radius, color=(0, 0, 0)):
        self.center = (y, x)
        self.radius = radius
        self.color = color


def executar(tamanho, circle, cor=None):
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    x, y, raio = circle.center, circle.radius, circle.radius
    cor = circle.color if cor is None else cor
    resultado = imagem.draw_circle(x, y, raio, cor)
    return resultado.image
