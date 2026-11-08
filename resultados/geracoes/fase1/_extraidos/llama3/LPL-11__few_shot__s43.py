from dataclasses import dataclass

@dataclass
class Disco:
    x: int
    y: int
    raio: int
    cor: tuple[int, int, int] = (0, 0, 0)

def executar(tamanho, disco: Disco):
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    resultado = imagem.draw_circle(disco.x, disco.y, disco.raio, disco.cor)
    return resultado.image
