"""Drawing of a segment on a grayscale image.

Public entry point: run(image, line). Do not change its name or signature;
the rest of the file may be freely reorganized.

The image starts all zeros; the line is marked with 1.
"""

import skimage
import numpy as np
from dataclasses import dataclass, asdict


@dataclass
class Line:
    """
    A class to represent a line.
    """
    y0: int
    x0: int
    y1: int
    x1: int


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

    def draw_line(self, line: Line):
        """
        Draw a line on the image.

        @param line: Line object representing the line to be drawn
        @return: image with line drawn on it
        """
        line_coords = skimage.draw.line(line.y0, line.x0, line.y1, line.x1)
        self.image[line_coords] = 1
        return self


def run(size, line: Line):
    """size: 2D tuple (rows, columns). line: 4D tuple (y0, x0, y1, x1). 
    Public entry point of this unit."""
    image = Image(np.zeros(size))
    result = image.draw_line(line)
    return result.image
