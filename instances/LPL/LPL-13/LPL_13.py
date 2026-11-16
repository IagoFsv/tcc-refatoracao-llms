"""Bilinear interpolation of a point inside a rectangle.

Public entry point: run(point, corners, values). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""


def bilinear_interpolation(x, y, x1, x2, y1, y2, z11, z12, z21, z22):
    """Bilinear interpolation. It considers the values of the four points
    around the point to be interpolated and returns the interpolated value.
    Made with a lot of help from GitHub Copilot.

    Parameters
    ----------
    x : float
        x coordinate to which the value will be interpolated.
    y : float
        y coordinate to which the value will be interpolated.
    x1 : float
        x coordinate of the first point.
    x2 : float
        x coordinate of the second point.
    y1 : float
        y coordinate of the first point.
    y2 : float
        y coordinate of the second point.
    z11 : float
        Value at the first point.
    z12 : float
        Value at the second point.
    z21 : float
        Value at the third point.
    z22 : float
        Value at the fourth point.

    Returns
    -------
    float
        Interpolated value.

    Examples
    --------
    >>> from rocketpy.tools import bilinear_interpolation
    >>> bilinear_interpolation(0.5, 0.5, 0, 1, 0, 1, 0, 1, 1, 0)
    0.5
    """
    return (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))


def run(point, corners, values):
    """point: (x, y). corners: (x1, x2, y1, y2). values: (z11, z12, z21, z22). Public entry point of this unit."""
    x, y = point
    x1, x2, y1, y2 = corners
    z11, z12, z21, z22 = values
    return bilinear_interpolation(x, y, x1, x2, y1, y2, z11, z12, z21, z22)
