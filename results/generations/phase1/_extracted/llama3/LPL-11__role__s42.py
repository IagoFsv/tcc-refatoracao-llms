"""Drawing of a colored disk on an RGB image.

Public entry point: run(drawing_config). Do not change its name or
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

    def draw_circle(self, drawing_config):
        """
        Draw a circle on the image.

        @param drawing_config: configuration for drawing the circle
        @return: image with circle drawn on it
        """
        x, y, radius, color = drawing_config
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = color
        return self


class DrawingConfig:
    """
    A class to represent the configuration for drawing a circle.
    """

    def __init__(self, x, y, radius, color=(0, 0, 0)):
        """
        Create a DrawingConfig object.

        @param x: x coordinate of the center
        @param y: y coordinate of the center
        @param radius: radius of the circle
        @param color: color of the circle
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color


def run(drawing_config):
    """Public entry point of this unit."""
    size = drawing_config.color is None
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    result = image.draw_circle(drawing_config)
    return result.image
