"""Bilinear interpolation of a point inside a rectangle.

Public entry point: run(point, corners, values). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""


class PointValues:
    """Class to hold the point values."""

    def __init__(self, z11, z12, z21, z22):
        """Initialize the point values.

        Parameters
        ----------
        z11  : float
            Value at the first point.
        z12  : float
            Value at the second point.
        z21  : float
            Value at the third point.
        z22  : float
            Value at the fourth point.
        """
        self.z11 = z11
        self.z12 = z12
        self.z21 = z21
        self.z22 = z22


class CornerPoints:
    """Class to hold the corner points."""

    def __init__(self, x1, x2, y1, y2):
        """Initialize the corner points.

        Parameters
        ----------
        x1  : float
            x coordinate of the first point.
        x2  : float
            x coordinate of the second point.
        y1  : float
            y coordinate of the first point.
        y2  : float
            y coordinate of the second point.
        """
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


def bilinear_interpolation(x, y, corners, values):
    """Bilinear interpolation. It considers the values of the four points
    around the point to be interpolated and returns the interpolated value.
    Made with a lot of help from GitHub Copilot.

    Parameters
    ----------
    x  : float
        x coordinate to which the value will be interpolated.
    y  : float
        y coordinate to which the value will be interpolated.
    corners  : CornerPoints
        The corner points.
    values  : PointValues
        The point values.

    Returns
    -------
    float
        Interpolated value.

    Examples
    --------
    >>> from rocketpy.tools import bilinear_interpolation
    >>> bilinear_interpolation(0.5, 0.5, CornerPoints(0, 1, 0, 1), PointValues(0, 1, 1, 0))
    0.5
    """
    return (
        values.z11 * (corners.x2 - x) * (corners.y2 - y)
        + values.z21 * (x - corners.x1) * (corners.y2 - y)
        + values.z12 * (corners.x2 - x) * (y - corners.y1)
        + values.z22 * (x - corners.x1) * (y - corners.y1)
    ) / ((corners.x2 - corners.x1) * (corners.y2 - corners.y1))


def run(point, corners, values):
    """point:  (x, y). corners:  (x1, x2, y1, y2). values:  (z11, z12, z21, z22). Public entry point of this unit."""
    x, y = point
    corners = CornerPoints(corners[0], corners[1], corners[2], corners[3])
    values = PointValues(values[0], values[1], values[2], values[3])
    return bilinear_interpolation(x, y, corners, values)
