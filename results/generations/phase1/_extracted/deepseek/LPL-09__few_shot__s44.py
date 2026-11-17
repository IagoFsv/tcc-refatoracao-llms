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

    def draw_line(self, line_info):
        """
        Draw a line on the image.

        @param line_info: LineInfo object representing the line to draw
        @return: image with line drawn on it
        """
        line = skimage.draw.line(line_info.y0, line_info.x0, line_info.y1, line_info.x1)
        self.image[line] = 1
        return self


@dataclass
class LineInfo:
    y0: int
    x0: int
    y1: int
    x1: int


def run(size, segment):
    """size: 2-tuple (rows, columns). segment: 4-tuple (y0, x0, y1, x1). Public entry point of this unit."""
    image = Image(np.zeros(size))
    line_info = LineInfo(*segment)
    result = image.draw_line(line_info)
    return result.image
