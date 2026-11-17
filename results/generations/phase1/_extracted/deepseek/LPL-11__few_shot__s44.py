from dataclasses import dataclass, asdict
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

    def draw_circle(self, circle_params: dataclass):
        """
        Draw a circle on the image.

        @param circle_params: dataclass containing parameters for the circle
        @return: image with circle drawn on it
        """
        circle = skimage.draw.disk((circle_params.y, circle_params.x), circle_params.radius, shape=self.image.shape)
        self.image[circle] = asdict(circle_params.color)
        return self


@dataclass
class CircleParams:
    x: int
    y: int
    radius: int
    color: tuple


def run(size, disk, color=None):
    """size:  (rows, columns). disk:  (x, y, radius). color:  (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    x, y, radius = disk
    if color is None:
        result = image.draw_circle(CircleParams(x, y, radius, (0, 0, 0)))
    else:
        result = image.draw_circle(CircleParams(x, y, radius, color))
    return result.image
