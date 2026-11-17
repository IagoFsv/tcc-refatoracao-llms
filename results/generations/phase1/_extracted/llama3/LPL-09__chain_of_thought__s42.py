"""Drawing of a segment on a grayscale image.

Public entry point: run(size, segment). Do not change its name or signature;
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

    def draw_line(self, segment):
        """
        Draw a line on the image.

        @param segment: Segment object representing the line segment
        @return: image with line drawn on it
        """
        line = skimage.draw.line(segment.start.y, segment.start.x, segment.end.y, segment.end.x)
        self.image[line] = 1
        return self


class Segment:
    """
    A class to represent a line segment.
    """

    def __init__(self, start, end):
        """
        Create a Segment object from start and end points.

        @param start: Point object representing the start point
        @param end: Point object representing the end point
        """
        self.start = start
        self.end = end


class Point:
    """
    A class to represent a point.
    """

    def __init__(self, y, x):
        """
        Create a Point object from y and x coordinates.

        @param y: y coordinate
        @param x: x coordinate
        """
        self.y = y
        self.x = x


def run(size, segment):
    """size: (rows, columns). segment: Segment object. Public entry point of this unit."""
    image = Image(np.zeros(size))
    result = image.draw_line(segment)
    return result.image
