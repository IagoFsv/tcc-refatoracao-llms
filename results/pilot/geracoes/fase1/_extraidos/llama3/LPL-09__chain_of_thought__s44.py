class Image:
    # ...

    def draw_line(self, y0, x0, y1, x1):
        # ...

class Segment:
    def __init__(self, y0, x0, y1, x1):
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1

def executar(tamanho, segmento):
    imagem = Image(np.zeros(tamanho))
    resultado = imagem.draw_line(segmento.y0, segmento.x0, segmento.y1, segmento.x1)
    return resultado.image
