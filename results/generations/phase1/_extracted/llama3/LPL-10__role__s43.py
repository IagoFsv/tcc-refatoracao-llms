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

    def draw_line(self, coordinates, color=(0, 0, 0)):
        """
        Draw a line on the image.

        @param coordinates: tuple of (y0, x0, y1, x1)
        @param color: color of the line
        @return: image with line drawn on it
        """
        y0, x0, y1, x1 = coordinates
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = color
        return self


def run(size, segment, color=None):
    """size: (rows, columns). segment: (y0, x0, y1, x1). color: (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    if color is None:
        result = image.draw_line(segment, color)
    else:
        result = image.draw_line(segment, color)
    return result.image
