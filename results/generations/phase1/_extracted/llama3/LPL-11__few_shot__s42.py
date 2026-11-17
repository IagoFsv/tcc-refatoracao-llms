"""Drawing of a colored disk on an RGB image.

Public entry point: run(size, disk). Do not change its name or
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

    def draw_circle(self, circle_info):
        """
        Draw a circle on the image.

        @param circle_info: CircleDrawingInfo object
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk(circle_info.center, circle_info.radius, shape=self.image.shape)
        self.image[circle] = circle_info.color
        return self

class CircleDrawingInfo:
    """
    Circle drawing information.
    """

    def __init__(self, x, y, radius, color=(0, 0, 0)):
        """
        Create a CircleDrawingInfo object.

        @param x: x coordinate of the center
        @param y: y coordinate of the center
        @param radius: radius of the circle
        @param color: color of the circle
        """
        self.center = (y, x)
        self.radius = radius
        self.color = color

def run(size, disk_info):
    """size: (rows, columns). disk_info: CircleDrawingInfo. Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    if disk_info.color is None:
        result = image.draw_circle(disk_info)
    else:
        result = image.draw_circle(disk_info)
    return result.image
