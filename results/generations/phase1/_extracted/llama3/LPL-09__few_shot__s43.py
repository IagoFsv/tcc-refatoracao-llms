import skimage
import numpy as np
from dataclasses import dataclass, asdict

@dataclass
class Segment:
    y0: int
    x0: int
    y1: int
    x1: int

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

    def draw_line(self, segment: Segment):
        """
        Draw a line on the image.

        @param segment: Segment object
        @return: image with line drawn on it
        """
        line = skimage.draw.line(segment.y0, segment.x0, segment.y1, segment.x1)
        self.image[line] = 1
        return self


def run(size, segment: Segment):
    """size: (rows, columns). segment: Segment object. Public entry point of this unit."""
    image = Image(np.zeros(size))
    result = image.draw_line(segment)
    return result.image
