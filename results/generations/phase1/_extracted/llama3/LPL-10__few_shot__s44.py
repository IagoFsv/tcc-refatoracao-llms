"""Drawing of a colored segment on an RGB image.

Public entry point: run(size, segment, color=None). Do not change its name or
signature; the rest of the file may be freely reorganized.

The image starts all white (255 in the three channels). Without a color, the
default color of the drawing applies.
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


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    def draw_line(self, line_segment, color=(0, 0, 0)):
        """
        Draw a line on the image.

        @param line_segment: LineSegment object
        @param color: color of the line
        @return: image with line drawn on it
        """
        line = skimage.draw.line(line_segment.y0, line_segment.x0, line_segment.y1, line_segment.x1)
        self.image[line] = color
        return self


@dataclass
class LineSegment:
    y0: int
    x0: int
    y1: int
    x1: int


def run(size, segment: LineSegment, color=None):
    """size: (rows, columns). segment: LineSegment. color: (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    if color is None:
        result = image.draw_line(segment)
    else:
        result = image.draw_line(segment, color)
    return result.image
