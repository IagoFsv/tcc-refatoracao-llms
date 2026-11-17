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

    def draw_line(self, line):
        """
        Draw a line on the image.

        @param line: Line object representing the line to be drawn
        @return: image with line drawn on it
        """
        self.image[skimage.draw.line(*line)] = line.color
        return self


@dataclass
class Line:
    y0: int
    x0: int
    y1: int
    x1: int
    color: tuple = (0, 0, 0)


def run(size, segment, color=None):
    """size:  (rows, columns). segment:  (y0, x0, y1, x1). color:  (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    line = Line(*segment, color if color else (0, 0, 0))
    result = image.draw_line(line)
    return result.image
