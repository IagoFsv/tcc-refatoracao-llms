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


class Disk:
    """
    A class to represent a disk.
    """

    def __init__(self, x, y, radius, color=(0, 0, 0)):
        """
        Create a Disk object.

        @param x: x coordinate of the center
        @param y: y coordinate of the center
        @param radius: radius of the circle
        @param color: color of the circle
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    def draw_circle(self, disk):
        """
        Draw a circle on the image.

        @param disk: Disk object
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk((disk.y, disk.x), disk.radius, shape=self.image.shape)
        self.image[circle] = disk.color
        return self


def run(size, disk, color=None):
    """size: (rows, columns). disk: (x, y, radius). color: (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    if color is None:
        disk = Disk(*disk)
    else:
        disk = Disk(*disk, color)
    result = image.draw_circle(disk)
    return result.image
