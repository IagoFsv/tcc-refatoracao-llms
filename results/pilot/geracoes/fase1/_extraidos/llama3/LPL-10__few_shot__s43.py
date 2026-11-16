from dataclasses import dataclass

@dataclass
class Segmento:
    y0: int
    x0: int
    y1: int
    x1: int

    def __init__(self, y0, x0, y1, x1):
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1

@dataclass
class Cor:
    r: int
    g: int
    b: int

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

def executar(tamanho, segmento: Segmento, cor: Cor = None):
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = segmento.y0, segmento.x0, segmento.y1, segmento.x1
    if cor is None:
        resultado = imagem.draw_line(y0, x0, y1, x1)
    else:
        resultado = imagem.draw_line(y0, x0, y1, x1, (cor.r, cor.g, cor.b))
    return resultado.image
