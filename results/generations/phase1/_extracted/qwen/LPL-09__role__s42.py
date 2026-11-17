"""Drawing of a segment on a grayscale image.

Public entry point: run(size, segment). Do not change its name or signature;
the rest of the file may be freely reorganized.

The image starts all zeros; the segment is marked with 1.
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

    def draw_line(self, y0, x0, y1, x1):
        """
        Draw a line on the image.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        @return: image with line drawn on it
        """
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = 1
        return self


class DrawingParameters:
    """Class to hold drawing parameters."""

    def __init__(self, y0, x0, y1, x1):
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1


def run(size, segment):
    """size: (rows, columns). segment: (y0, x0, y1, x1). Public entry point of this unit."""
    image = Image(np.zeros(size))
    drawing_params = DrawingParameters(*segment)
    result = image.draw_line(drawing_params.y0, drawing_params.x0, drawing_params.y1, drawing_params.x1)
    return result.image
