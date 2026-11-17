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


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    @dataclass
    class Segment:
        y0: int
        x0: int
        y1: int
        x1: int
        color: tuple = (0, 0, 0)

    def draw_line(self, segment: Segment):
        """
        Draw a line on the image.

        @param segment: segment to draw
        @return: image with line drawn on it
        """
        line = skimage.draw.line(segment.y0, segment.x0, segment.y1, segment.x1)
        self.image[line] = segment.color
        return self

def run(size, segment: RGB_Image.Segment):
    """size: (rows, columns). segment: segment to draw. Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    result = image.draw_line(segment)
    return result.image
