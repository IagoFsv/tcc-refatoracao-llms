from dataclasses import dataclass

@dataclass
class Linha:
    y0: int
    x0: int
    y1: int
    x1: int
    cor: tuple = (0, 0, 0)

def executar(tamanho, linha: Linha):
    """tamanho: (linhas, colunas). linha: Linha."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = linha.y0, linha.x0, linha.y1, linha.x1
    cor = linha.cor
    resultado = imagem.draw_line(y0, x0, y1, x1, cor)
    return resultado.image
