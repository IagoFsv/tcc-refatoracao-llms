from dataclasses import dataclass

@dataclass
class Segmento:
    y0: int
    x0: int
    y1: int
    x1: int

@dataclass
class Cor:
    r: int
    g: int
    b: int

def executar(tamanho: tuple, segmento: Segmento, cor: Cor = None):
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    if cor is None:
        resultado = imagem.draw_line(segmento.y0, segmento.x0, segmento.y1, segmento.x1)
    else:
        resultado = imagem.draw_line(segmento.y0, segmento.x0, segmento.y1, segmento.x1, (cor.r, cor.g, cor.b))
    return resultado.image
