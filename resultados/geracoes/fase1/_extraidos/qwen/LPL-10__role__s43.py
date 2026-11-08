import skimage
import numpy as np

class Image:
    """
    A class to represent an image.
    """

    def __init__(self, array):
        """
        Create an Image object from a numpy array.

        @param array: numpy array representing the image
        """
        self.image = array


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    def draw_line(self, segment, color=(0, 0, 0)):
        """
        Draw a line on the image.

        @param segment: tuple containing the coordinates of the two points (y0, x0, y1, x1)
        @param color: color of the line
        @return: image with line drawn on it
        """
        y0, x0, y1, x1 = segment
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = color
        return self


def executar(tamanho, segmento, cor=None):
    """tamanho: (linhas, colunas). segmento: (y0, x0, y1, x1). cor: (r, g, b)."""
    imagem = RGB_Image(np.full((*tamanho, 3), 255, dtype=np.uint8))
    resultado = imagem.draw_line(segmento, cor)
    return resultado.image
