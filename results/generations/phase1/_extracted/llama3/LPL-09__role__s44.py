"""Drawing of a segment on a grayscale image.

Public entry point: run(segment). Do not change its name or signature;
the rest of the file may be freely reorganized.

The image starts all zeros; the segment is marked with 1.
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

    def draw_line(self, coordinates):
        """
        Draw a line on the image.

        @param coordinates: Dictionary with 'y0', 'x0', 'y1', 'x1' points
        @return: image with line drawn on it
        """
        y0, x0, y1, x1 = coordinates.values()
        line = skimage.draw.line(y0, x0, y1, x1)
        self.image[line] = 1
        return self


class Segment:
    """
    A class to represent a segment.
    """

    def __init__(self, y0, x0, y1, x1):
        """
        Create a Segment object.

        @param y0: y coordinate of the first point
        @param x0: x coordinate of the first point
        @param y1: y coordinate of the second point
        @param x1: x coordinate of the second point
        """
        self.coordinates = {'y0': y0, 'x0': x0, 'y1': y1, 'x1': x1}


def run(segment):
    """Public entry point of this unit."""
    size = (segment.coordinates['y1'] + 1, segment.coordinates['x1'] + 1)
    image = Image(np.zeros(size))
    result = image.draw_line(segment.coordinates)
    return result.image
