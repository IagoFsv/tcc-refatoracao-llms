import skimage
import numpy as np

class Image:
    # ...

class RGB_Image(Image):
    # ...

class DrawingOptions:
    def __init__(self, size, segment, color=None):
        self.size = size
        self.segment = segment
        self.color = color

def executar(options):
    imagem = RGB_Image(np.full((*options.size, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = options.segment
    if options.color is None:
        resultado = imagem.draw_line(y0, x0, y1, x1)
    else:
        resultado = imagem.draw_line(y0, x0, y1, x1, options.color)
    return resultado.image

# Exemplo de uso:
options = DrawingOptions((10, 10), (0, 0, 9, 9), (255, 0, 0))
resultado = executar(options)
