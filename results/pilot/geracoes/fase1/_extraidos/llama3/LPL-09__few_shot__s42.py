from dataclasses import dataclass

@dataclass
class Segmento:
    y0: int
    x0: int
    y1: int
    x1: int

def executar(tamanho: tuple, segmento: Segmento):
    imagem = Image(np.zeros(tamanho))
    resultado = imagem.draw_line(segmento.y0, segmento.x0, segmento.y1, segmento.x1)
    return resultado.image
