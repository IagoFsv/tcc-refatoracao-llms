"""Bilinear interpolation of a point inside a rectangle.

Public entry point: run(point, rectangle, values). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from dataclasses import dataclass, asdict

@dataclass
class Rectangle:
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

def bilinear_interpolation(x, y, rectangle, values):
    """Bilinear interpolation. It considers the values of the four points
    around the point to be interpolated and returns the interpolated value.
    Made with a lot of help from GitHub Copilot.

    Parameters
    ----------
    x : float
        x coordinate to which the value will be interpolated.
    y : float
        y coordinate to which the value will be interpolated.
    rectangle : Rectangle
        Coordinates of the rectangle corners.
    values : Values
        Values at the four points around the point to be interpolated.

    Returns
    -------
    float
        Interpolated value.

    Examples
    --------
    >>> from rocketpy.tools import bilinear_interpolation
    >>> bilinear_interpolation(0.5, 0.5, Rectangle(0, 1, 0, 1), Values(0, 1, 1, 0))
    0.5
    """
    return (
        values.z11 * (rectangle.x2 - x) * (rectangle.y2 - y)
        + values.z21 * (x - rectangle.x1) * (rectangle.y2 - y)
        + values.z12 * (rectangle.x2 - x) * (y - rectangle.y1)
        + values.z22 * (x - rectangle.x1) * (y - rectangle.y1)
    ) / ((rectangle.x2 - rectangle.x1) * (rectangle.y2 - rectangle.y1))


def run(point, rectangle, values):
    """point: (x, y). rectangle: Rectangle. values: Values. Public entry point of this unit."""
    x, y = point
    return bilinear_interpolation(x, y, rectangle, values)
