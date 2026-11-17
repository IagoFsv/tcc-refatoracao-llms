"""Drawing of a colored segment on an RGB image.

Public entry point: run(image_size, line_segment, line_color=None). Do not change its name or
signature; the rest of the file may be freely reorganized.

The image starts all white  (255 in the three channels). Without a color, the
default color of the drawing applies.
"""

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

    def draw_line(self, line_parameters):
        """
        Draw a line on the image.

        @param line_parameters: object containing line parameters
        @return: image with line drawn on it
        """
        line = skimage.draw.line(*line_parameters)
        self.image[line] = line_parameters.color
        return self


class LineParameters:
    """
    A class to represent line parameters.
    """

    def __init__(self, y0, x0, y1, x1, color=(0, 0, 0)):
        """
        Create a LineParameters object.

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


def run(image_size, line_segment, line_color=None):
    """image_size: (rows, columns). line_segment: (y0, x0, y1, x1). line_color: (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*image_size, 3), 255, dtype=np.uint8))
    y0, x0, y1, x1 = line_segment
    if line_color is None:
        result = image.draw_line(LineParameters(y0, x0, y1, x1))
    else:
        result = image.draw_line(LineParameters(y0, x0, y1, x1, line_color))
    return result.image
