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

    def draw_line(self, line):
        """
        Draw a line on the image.

        @param line: tuple (y0, x0, y1, x1) representing the line
        @return: image with line drawn on it
        """
        line = skimage.draw.line(*line)
        self.image[line] = 1
        return self


def run(size, segment):
    """size: (rows, columns). segment: (y0, x0, y1, x1). Public entry point of this unit."""
    image = Image(np.zeros(size))
    result = image.draw_line(segment)
    return result.image
