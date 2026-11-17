"""Bilinear interpolation of a point inside a rectangle.

Public entry point: run(point, corners, values). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

class PointValues:
    """Class to encapsulate the values of a point."""
    def __init__(self, z11, z12, z21, z22):
        self.z11 = z11
        self.z12 = z12
        self.z21 = z21
        self.z22 = z22


class CornerPoints:
    """Class to encapsulate the corner points."""
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


def bilinear_interpolation(x, y, corner_points, point_values):
    """Bilinear interpolation. It considers the values of the four points
    around the point to be interpolated and returns the interpolated value.
    Made with a lot of help from GitHub Copilot.

    Parameters
    ----------
    x  : float
         x coordinate to which the value will be interpolated.
    y  : float
         y coordinate to which the value will be interpolated.
    corner_points : CornerPoints
                    Object containing the corner points.
    point_values  : PointValues
                    Object containing the values of the point.

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
    x1, x2, y1, y2 = corner_points.x1, corner_points.x2, corner_points.y1, corner_points.y2
    z11, z12, z21, z22 = point_values.z11, point_values.z12, point_values.z21, point_values.z22
    return  (
        z11  *  (x2  - x)  *  (y2  - y)
        + z21  *  (x  - x1)  *  (y2  - y)
        + z12  *  (x2  - x)  *  (y  - y1)
        + z22  *  (x  - x1)  *  (y  - y1)
    )  /  ((x2  - x1)  *  (y2  - y1))


def run(point, corners, values):
    """point:  (x, y). corners:  (x1, x2, y1, y2). values:  (z11, z12, z21, z22). Public entry point of this unit."""
    x, y  = point
    corner_points = CornerPoints(*corners)
    point_values = PointValues(*values)
    return bilinear_interpolation(x, y, corner_points, point_values)
