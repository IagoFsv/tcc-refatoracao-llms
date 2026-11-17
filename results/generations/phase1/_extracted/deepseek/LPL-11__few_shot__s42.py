"""Drawing of a colored disk on an RGB image.

Public entry point: run(disk_info). Do not change its name or
signature; the rest of the file may be freely reorganized.

The image starts all white (255 in the three channels). Without a color, the
default color of the drawing applies. The disk is clipped at the image border.
"""

import skimage
import numpy as np
from dataclasses import dataclass, asdict


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


@dataclass
class DiskInfo:
    """
    Dataclass to hold disk information.
    """
    size: tuple
    disk: tuple
    color: tuple = None


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    def draw_circle(self, disk_info: DiskInfo):
        """
        Draw a circle on the image.

        @param disk_info: DiskInfo object containing the information about the disk to be drawn
        @return: image with circle drawn on it
        """
        x, y, radius = disk_info.disk
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        color = disk_info.color if disk_info.color else (0, 0, 0)
        self.image[circle] = color
        return self


def run(disk_info: DiskInfo):
    """disk_info: DiskInfo object. Public entry point of this unit."""
    image = RGB_Image(np.full((*disk_info.size, 3), 255, dtype=np.uint8))
    result = image.draw_circle(disk_info)
    return result.image
