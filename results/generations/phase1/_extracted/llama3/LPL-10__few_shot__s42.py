"""Drawing of a colored segment on an RGB image.

Public entry point: run(size, segment). Do not change its name or
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

    def draw_line(self, segment, color=(0, 0, 0)):
        """
        Draw a line on the image.

        @param segment: (y0, x0, y1, x1)
        @param color: color of the line
        @return: image with line drawn on it
        """
        y0, x0, y1, x1 = segment
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = color
        return self


class Segment:
    """
    A class to represent a segment.
    """

    def __init__(self, y0, x0, y1, x1):
        """
        Create a Segment object.

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
    """size: (rows, columns). segment: Segment. Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    if segment is not None:
        result = image.draw_line((segment.y0, segment.x0, segment.y1, segment.x1), segment.color if hasattr(segment, 'color') else (0, 0, 0))
    else:
        result = image
    return result.image
