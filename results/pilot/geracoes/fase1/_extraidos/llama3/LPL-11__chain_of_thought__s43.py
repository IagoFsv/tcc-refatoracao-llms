class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

def executar(tamanho, circle, color=None):
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    if color is None:
        resultado = imagem.draw_circle(circle.x, circle.y, circle.radius)
    else:
        resultado = imagem.draw_circle(circle.x, circle.y, circle.radius, (color.r, color.g, color.b))
    return resultado.image
