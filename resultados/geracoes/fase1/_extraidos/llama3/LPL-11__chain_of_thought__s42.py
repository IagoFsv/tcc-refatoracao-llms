class Circle:
    def __init__(self, x, y, radius, color=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

def executar(tamanho, circle):
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    if circle.color is None:
        resultado = imagem.draw_circle(circle.x, circle.y, circle.radius)
    else:
        resultado = imagem.draw_circle(circle.x, circle.y, circle.radius, circle.color)
    return resultado.image
