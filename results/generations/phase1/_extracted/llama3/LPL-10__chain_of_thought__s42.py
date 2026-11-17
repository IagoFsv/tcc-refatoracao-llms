"""Drawing of a colored segment on an RGB image.

Public entry point: run(size, segment, color=None). Do not change its name or
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

    def draw_line(self, segment, color=None):
        """
        Draw a line on the image.

        @param segment: Segment object
        @param color: Color object
        @return: image with line drawn on it
        """
        y0, x0, y1, x1 = segment.y0, segment.x0, segment.y1, segment.x1
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = color.rgb if color is not None else (0, 0, 0)
        return self


class Segment:
    """
    A class to represent a segment.
    """

    def __init__(self, y0, x0, y1, x1):
        """
        Create a Segment object from y0, x0, y1, x1.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        """
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1


class Color:
    """
    A class to represent a color.
    """

    def __init__(self, rgb):
        """
        Create a Color object from rgb.

        @param rgb: rgb color
        """
        self.rgb = rgb


def run(size, segment, color=None):
    """size: (rows, columns). segment: Segment object. color: Color object. Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    if color is None:
        result = image.draw_line(Segment(*segment), Color((0, 0, 0)))
    else:
        result = image.draw_line(Segment(*segment), Color(color))
    return result.image
