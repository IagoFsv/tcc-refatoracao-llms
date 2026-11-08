class DrawOptions:
    def __init__(self, tamanho, segmento, cor=None):
        self.tamanho = tamanho
        self.segmento = segmento
        self.cor = cor

def executar(options):
    imagem = RGB_Image(np.full((*options.tamanho, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = options.segmento
    if options.cor is None:
        resultado = imagem.draw_line(y0, x0, y1, x1)
    else:
        resultado = imagem.draw_line(y0, x0, y1, x1, options.cor)
    return resultado.image
