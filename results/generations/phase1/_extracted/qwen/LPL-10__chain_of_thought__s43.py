"""Drawing of a colored segment on an RGB image.

Public entry point: run(drawing_params). Do not change its name or
signature; the rest of the file may be freely reorganized.

The image starts all white (255 in the three channels). Without a color, the
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

    def draw_line(self, y0, x0, y1, x1, color=(0, 0, 0)):
        """
        Draw a line on the image.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        @param color: color of the line
        @return: image with line drawn on it
        """
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = color
        return self


class DrawingParameters:
    """
    Class to encapsulate drawing parameters.
    """

    def __init__(self, size, segment, color=None):
        """
        Initialize the DrawingParameters object.

        @param size: (rows, columns)
        @param segment: (y0, x0, y1, x1)
        @param color: (r, g, b)
        """
        self.size = size
        self.segment = segment
        self.color = color


def run(drawing_params):
    """Public entry point of this unit."""
    image = RGB_Image(np.full(drawing_params.size, 255, dtype=np.uint8))
    y0, x0, y1, x1 = drawing_params.segment
    if drawing_params.color is None:
        result = image.draw_line(y0, x0, y1, x1)
    else:
        result = image.draw_line(y0, x0, y1, x1, drawing_params.color)
    return result.image
