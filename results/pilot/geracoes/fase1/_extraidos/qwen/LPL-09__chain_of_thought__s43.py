import skimage
import numpy as np

class ImageSize:
    def __init__(self, linhas, colunas):
        self.linhas = linhas
        self.colunas = colunas

class LineSegment:
    def __init__(self, y0, x0, y1, x1):
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1

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

    def draw_line(self, line_segment):
        """
        Draw a line on the image.

        @param line_segment: LineSegment object representing the line to draw
        @return: image with line drawn on it
        """
        line = skimage.draw.line(line_segment.y0, line_segment.x0, line_segment.y1, line_segment.x1)
        self.image[line] = 1
        return self


def executar(image_size, line_segment):
    """image_size: ImageSize object. line_segment: LineSegment object."""
    imagem = Image(np.zeros((image_size.linhas, image_size.colunas)))
    resultado = imagem.draw_line(line_segment)
    return resultado.image
