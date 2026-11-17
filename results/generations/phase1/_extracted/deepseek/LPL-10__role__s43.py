"""Drawing of a colored segment on an RGB image.

Public entry point: run(image_size, line_segment, line_color=None). Do not change its name or
signature; the rest of the file may be freely reorganized.

The image starts all white  (255 in the three channels). Without a color, the
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

    def draw_line(self, line_segment, line_color=(0, 0, 0)):
        """
        Draw a line on the image.

        @param line_segment: a tuple representing the line segment (y0, x0, y1, x1)
        @param line_color: color of the line
        @return: image with line drawn on it
        """
        y0, x0, y1, x1 = line_segment
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = line_color
        return self


def run(image_size, line_segment, line_color=None):
    """image_size: (rows, columns). line_segment: (y0, x0, y1, x1). line_color: (r, g, b). Public entry point of this unit."""
    image = RGB_Image(np.full((*image_size, 3), 255, dtype=np.uint8))
    if line_color is None:
        result = image.draw_line(line_segment)
    else:
        result = image.draw_line(line_segment, line_color)
    return result.image
