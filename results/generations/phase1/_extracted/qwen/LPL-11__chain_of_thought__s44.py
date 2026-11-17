"""Drawing of a colored disk on an RGB image.

Public entry point: run(draw_params). Do not change its name or
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

    def draw_circle(self, x, y, radius, color=(0, 0, 0)):
        """
        Draw a circle on the image.

        @param x: x coordinate of the center
        @param y: y coordinate of the center
        @param radius: radius of the circle
        @param color: color of the circle
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = color
        return self


class DrawParameters:
    """
    Class to hold parameters for drawing a circle.
    """

    def __init__(self, size, disk, color=None):
        """
        Create a DrawParameters object.

        @param size: tuple (rows, columns)
        @param disk: tuple (x, y, radius)
        @param color: tuple (r, g, b) or None
        """
        self.size = size
        self.disk = disk
        self.color = color


def run(draw_params):
    """Public entry point of this unit."""
    image = RGB_Image(np.full(draw_params.size, 255, dtype=np.uint8))
    x, y, radius = draw_params.disk
    if draw_params.color is None:
        result = image.draw_circle(x, y, radius)
    else:
        result = image.draw_circle(x, y, radius, draw_params.color)
    return result.image
