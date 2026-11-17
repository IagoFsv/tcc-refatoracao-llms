import skimage
import numpy as np
from dataclasses import dataclass, asdict

@dataclass
class Disk:
    x: int
    y: int
    radius: int
    color: tuple = (0, 0, 0)

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

    def draw_circle(self, disk):
        """
        Draw a circle on the image.

        @param disk: Disk object
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk((disk.y, disk.x), disk.radius, shape=self.image.shape)
        self.image[circle] = disk.color
        return self


def run(size, disk):
    """size: (rows, columns). disk: Disk object. Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    result = image.draw_circle(disk)
    return result.image
