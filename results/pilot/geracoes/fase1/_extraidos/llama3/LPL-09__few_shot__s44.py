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

    def draw_line(self, segment: "Segment"):
        """
        Draw a line on the image.

        @param segment: Segment object
        @return: image with line drawn on it
        """
        y0, x0, y1, x1 = segment
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = 1
        return self


@dataclass
class Segment:
    y0: int
    x0: int
    y1: int
    x1: int

def executar(tamanho: tuple, segment: Segment):
    imagem = Image(np.zeros(tamanho))
    resultado = imagem.draw_line(segment)
    return resultado.image
