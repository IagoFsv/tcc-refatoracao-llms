"""Drawing of a segment on a grayscale image.

Public entry point: run(segment). Do not change its name or signature;
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

    def draw_line(self, coordinates):
        """
        Draw a line on the image.

        @param coordinates: a tuple of coordinates (y0, x0, y1, x1)
        @return: image with line drawn on it
        """
        y0, x0, y1, x1 = coordinates
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = 1
        return self


@dataclass
class Segment:
    y0: int
    x0: int
    y1: int
    x1: int


def run(segment: Segment):
    """Public entry point of this unit."""
    size = (100, 100)  # assuming a default size
    image = Image(np.zeros(size))
    y0, x0, y1, x1 = segment
    result = image.draw_line((y0, x0, y1, x1))
    return result.image
