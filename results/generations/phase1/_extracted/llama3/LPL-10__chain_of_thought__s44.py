"""Drawing of a colored segment on an RGB image.

Public entry point: run(size, segment, color=None). Do not change its name or
signature; the rest of the file may be freely reorganized.

The image starts all white (255 in the three channels). Without a color, the
default color of the drawing applies.
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


class RGB_Image(Image):
    """
    RGB_Image class.
    """

    def __init__(self, array):
        super().__init__(array)

    def draw_line(self, segment):
        line = skimage.draw.line(segment.y0, segment.x0, segment.y1, segment.x1)
        self.image[line] = segment.color
        return self


class Segment:
    def __init__(self, y0, x0, y1, x1, color=(0, 0, 0)):
        self.y0 = y0
        self.x0 = x0
        self.y1 = y1
        self.x1 = x1
        self.color = color


def run(size, segment, color=None):
    """size: (rows, columns). segment: (y0, x0, y1, x1). color: (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    if color is None:
        result = image.draw_line(segment)
    else:
        result = image.draw_line(Segment(*segment, color=color))
    return result.image
