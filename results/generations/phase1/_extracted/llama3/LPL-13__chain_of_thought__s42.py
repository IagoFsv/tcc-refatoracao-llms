"""Bilinear interpolation of a point inside a rectangle.

Public entry point: run(point, corners, values). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Corner:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


def bilinear_interpolation(point, corner, value):
    """Bilinear interpolation. It considers the values of the four points
    around the point to be interpolated and returns the interpolated value.
    Made with a lot of help from GitHub Copilot.

    Parameters
    ----------
    point : Point
        Point to which the value will be interpolated.
    corner : Corner
        Corner of the rectangle.
    value : tuple
        Values at the four points.

    Returns
    -------
    float
        Interpolated value.

    Examples
    --------
    >>> from rocketpy.tools import bilinear_interpolation
    >>> corner = Corner(0, 1, 0, 1)
    >>> value = (0, 1, 1, 0)
    >>> bilinear_interpolation(Point(0.5, 0.5), corner, value)
    0.5
    """
    x, y = point.x, point.y
    x1, x2, y1, y2 = corner.x1, corner.x2, corner.y1, corner.y2
    z11, z12, z21, z22 = value
    return (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))


def run(point, corner, values):
    """point: (x, y). corners: (x1, x2, y1, y2). values: (z11, z12, z21, z22). Public entry point of this unit."""
    return bilinear_interpolation(point, corner, values)
