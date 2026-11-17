from dataclasses import dataclass, asdict
import skimage
import numpy as np


class Image:
    def __init__(self, array):
        self.image = array


class RGB_Image(Image):
    def draw_circle(self, x, y, radius, color=(0, 0, 0)):
        circle = skimage.draw.disk((y, x), radius, shape=self.image.shape)
        self.image[circle] = color
        return self


@dataclass
class Disk:
    x: int
    y: int
    radius: int
    color: tuple = (0, 0, 0)


def run(size, disk, color=None):
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    x, y, radius = disk
    if color is None:
        result = image.draw_circle(x, y, radius)
    else:
        result = image.draw_circle(x, y, radius, color)
    return result.image
