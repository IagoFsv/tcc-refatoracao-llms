"""Bilinear interpolation of a point inside a rectangle.

Public entry point: run(point, corners). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""


from dataclasses import dataclass, asdict

@dataclass
class Corner:
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

def bilinear_interpolation(x: float, y: float, corner: Corner, values: Values):
    """Bilinear interpolation. It considers the values of the four points
    around the point to be interpolated and returns the interpolated value.
    Made with a lot of help from GitHub Copilot.

    Parameters
    ----------
    x : float
        x coordinate to which the value will be interpolated.
    y : float
        y coordinate to which the value will be interpolated.
    corner : Corner
        The coordinates of the four points.
    values : Values
        The values at the four points.

    Returns
    -------
    float
        Interpolated value.

    Examples
    --------
    >>> from rocketpy.tools import bilinear_interpolation
    >>> bilinear_interpolation(0.5, 0.5, Corner(0, 1, 0, 1), Values(0, 1, 1, 0))
    0.5
    """
    return (
        values.z11 * (corner.x2 - x) * (corner.y2 - y)
        + values.z21 * (x - corner.x1) * (corner.y2 - y)
        + values.z12 * (corner.x2 - x) * (y - corner.y1)
        + values.z22 * (x - corner.x1) * (y - corner.y1)
    ) / ((corner.x2 - corner.x1) * (corner.y2 - corner.y1))


def run(point: tuple[float, float], corners: Corner, values: Values):
    """point: (x, y). corners: (x1, x2, y1, y2). values: (z11, z12, z21, z22). Public entry point of this unit."""
    x, y = point
    return bilinear_interpolation(x, y, corners, values)
