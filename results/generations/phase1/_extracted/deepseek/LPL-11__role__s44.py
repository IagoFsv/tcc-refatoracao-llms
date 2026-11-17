"""Drawing of a colored disk on an RGB image.

Public entry point: run(size, disk_params, color=None). Do not change its name or
signature; the rest of the file may be freely reorganized.

The image starts all white  (255 in the three channels). Without a color, the
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


class Disk:
    """
    A class to represent a disk.
    """

    def __init__(self, x, y, radius, color=(0, 0, 0)):
        """
        Create a Disk object.

        @param x: x coordinate of the center
        @param y: y coordinate of the center
        @param radius: radius of the disk
        @param color: color of the disk
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    def draw_disk(self, disk):
        """
        Draw a disk on the image.

        @param disk: Disk object representing the disk to be drawn
        @return: image with disk drawn on it
        """
        disk_circle = skimage.draw.disk((disk.y, disk.x), disk.radius, shape=self.image.shape)
        self.image[disk_circle] = disk.color
        return self


def run(size, disk_params, color=None):
    """size: (rows, columns). disk_params: (x, y, radius). color: (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    x, y, radius = disk_params
    if color is None:
        disk = Disk(x, y, radius)
    else:
        disk = Disk(x, y, radius, color)
    result = image.draw_disk(disk)
    return result.image
