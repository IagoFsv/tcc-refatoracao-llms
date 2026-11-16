import skimage
import numpy as np

class Image:
    def __init__(self, array):
        self.image = array

class RGB_Image(Image):
    def draw_circle(self, circle_params):
        x, y, radius, color = circle_params.x, circle_params.y, circle_params.radius, circle_params.color
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = color
        return self

class CircleParams:
    def __init__(self, x, y, radius, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

def executar(tamanho, disco, cor=None):
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    x, y, raio = disco
    if cor is None:
        resultado = imagem.draw_circle(CircleParams(x, y, raio))
    else:
        resultado = imagem.draw_circle(CircleParams(x, y, raio, cor))
    return resultado.image
