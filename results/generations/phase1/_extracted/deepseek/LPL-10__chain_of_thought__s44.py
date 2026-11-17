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

    def draw_line(self, line_params):
        """
        Draw a line on the image.

        @param line_params: Parameters for the line
        @return: image with line drawn on it
        """
        line = skimage.draw.line(line_params.y0, line_params.x0, line_params.y1, line_params.x1)
        self.image[line] = line_params.color
        return self


class LineParams:
    """
    Class to represent the parameters of a line.
    """

    def __init__(self, y0, x0, y1, x1, color=(0, 0, 0)):
        """
        Create a LineParams object.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        @param color: color of the line
        """
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1
        self.color = color


def run(size, segment, color=None):
    """size: (rows, columns). segment: (y0, x0, y1, x1). color: (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = segment
    if color is None:
        line_params = LineParams(y0, x0, y1, x1)
    else:
        line_params = LineParams(y0, x0, y1, x1, color)
    result = image.draw_line(line_params)
    return result.image
