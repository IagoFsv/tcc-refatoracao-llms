"""Bilinear interpolation of a point inside a rectangle.

Public entry point: run(point, corners, values). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from dataclasses import dataclass, asdict

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Corners:
    x1: float
    x2: float
    y1: float
    y2: float

@dataclass
class Values:
    z11: float
    z12: float
    z21: float
    z22: float

def bilinear_interpolation(point: Point, corners: Corners, values: Values):
    """Bilinear interpolation. It considers the values of the four points
    around the point to be interpolated and returns the interpolated value.
    Made with a lot of help from GitHub Copilot.

    Parameters
    ----------
    point  : Point
        Point to which the value will be interpolated.
    corners: Corners
        Corners of the rectangle.
    values : Values
        Values at the corners.

    Returns
    -------
    float
        Interpolated value.

    Examples
    --------
    >>> from rocketpy.tools import bilinear_interpolation
    >>> bilinear_interpolation(Point(0.5, 0.5), Corners(0, 1, 0, 1), Values(0, 1, 1, 0))
    0.5
    """
    x, y = point.x, point.y
    x1, x2, y1, y2 = corners.x1, corners.x2, corners.y1, corners.y2
    z11, z12, z21, z22 = values.z11, values.z12, values.z21, values.z22

    return  (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))


def run(point: Point, corners: Corners, values: Values):
    """point:  (x, y). corners:  (x1, x2, y1, y2). values:  (z11, z12, z21, z22). Public entry point of this unit."""
    return bilinear_interpolation(point, corners, values)
