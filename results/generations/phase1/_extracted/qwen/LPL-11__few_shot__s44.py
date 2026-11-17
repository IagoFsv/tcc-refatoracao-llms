"""Drawing of a colored disk on an RGB image.

Public entry point: run(size, disk, color=None). Do not change its name or
signature; the rest of the file may be freely reorganized.

The image starts all white (255 in the three channels). Without a color, the
default color of the drawing applies. The disk is clipped at the image border.
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

    def draw_circle(self, disk, color=(0, 0, 0)):
        """
        Draw a circle on the image.

        @param disk: (x, y, radius)
        @param color: color of the circle
        @return: image with circle drawn on it
        """
        x, y, radius = disk
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = color
        return self


def run(size, disk, color=None):
    """size: (rows, columns). disk: (x, y, radius). color: (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    result = image.draw_circle(disk, color)
    return result.image
