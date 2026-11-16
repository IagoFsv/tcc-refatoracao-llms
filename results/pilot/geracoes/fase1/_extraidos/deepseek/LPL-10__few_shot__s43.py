import skimage
import numpy as np
from dataclasses import dataclass, asdict

@dataclass
class Cor:
    r: int
    g: int
    b: int

@dataclass
class Ponto:
    y: int
    x: int

class Image:
    def __init__(self, array):
        self.image = array

class RGB_Image(Image):
    def draw_line(self, ponto1: Ponto, ponto2: Ponto, cor: Cor=None):
        if cor is None:
            cor = Cor(0, 0, 0)
        line = skimage.draw.line(ponto1.y, ponto1.x, ponto2.y, ponto2.x)
        self.image[line] = asdict(cor)
        return self

def executar(tamanho, segmento, cor=None):
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = segmento
    if cor is None:
        resultado = imagem.draw_line(Ponto(y0, x0), Ponto(y1, x1))
    else:
        resultado = imagem.draw_line(Ponto(y0, x0), Ponto(y1, x1), Cor(*cor))
    return resultado.image
