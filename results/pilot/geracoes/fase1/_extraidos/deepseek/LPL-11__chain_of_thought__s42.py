class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

class Image:
    ...

class RGB_Image(Image):
    ...
    def draw_circle(self, circle):
        circle_object = Circle(*circle)
        x, y, radius, color = circle_object.x, circle_object.y, circle_object.radius, circle_object.color
        ...

def executar(tamanho, disco, cor=None):
    ...
    if cor is None:
        resultado = imagem.draw_circle(disco)
    else:
        disco = (*disco, cor)
        resultado = imagem.draw_circle(disco)
    ...
