"""Drawing of a segment on a grayscale image.

Public entry point: run(image, line). Do not change its name or signature;
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

    def draw_line(self, line):
        """
        Draw a line on the image.

        @param line: line to be drawn
        @return: image with line drawn on it
        """
        self.image[skimage.draw.line(*line)] = 1
        return self


class Line:
    """
    A class to represent a line.
    """

    def __init__(self, y0, x0, y1, x1):
        """
        Create a Line object.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        """
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1


def run(size, segment):
    """size: 2-tuple (rows, columns). segment: 4-tuple (y0, x0, y1, x1).
    Public entry point of this unit."""
    image = Image(np.zeros(size))
    line = Line(*segment)
    result = image.draw_line(line)
    return result.image
