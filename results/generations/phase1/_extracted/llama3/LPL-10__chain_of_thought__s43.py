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
        """
        Create an RGB_Image object from a numpy array.

        @param array: numpy array representing the image
        """
        super().__init__(array)

    def draw_line(self, segment, color=None):
        """
        Draw a line on the image.

        @param segment: Segment object
        @param color: Color object or None
        @return: image with line drawn on it
        """
        line = skimage.draw.line(segment.y0, segment.x0, segment.y1, segment.x1)
        if color is None:
            self.image[line] = (0, 0, 0)
        else:
            self.image[line] = (color.r, color.g, color.b)
        return self

def run(size, segment, color=None):
    """size: (rows, columns). segment: Segment object. color: Color object or None. Public entry point of this unit."""
    image = RGB_Image(np.full((*size, 3), 255, dtype=np.uint8))
    if color is None:
        result = image.draw_line(segment, None)
    else:
        result = image.draw_line(segment, color)
    return result.image
