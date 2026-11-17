"""Bilinear interpolation of a point inside a rectangle.

Public entry point: run(point, corners, values). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""


class BilinearInterpolationData:
    def __init__(self, x1, x2, y1, y2, z11, z12, z21, z22):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z11 = z11
        self.z12 = z12
        self.z21 = z21
        self.z22 = z22

    def __call__(self, x, y):
        return (
            self.z11 * (self.x2 - x) * (self.y2 - y)
            + self.z21 * (x - self.x1) * (self.y2 - y)
            + self.z12 * (self.x2 - x) * (y - self.y1)
            + self.z22 * (x - self.x1) * (y - self.y1)
        ) / ((self.x2 - self.x1) * (self.y2 - self.y1))


def run(point, corners, values):
    """point: (x, y). corners: (x1, x2, y1, y2). values: (z11, z12, z21, z22). Public entry point of this unit."""
    x, y = point
    corners_data = BilinearInterpolationData(*corners)
    values_data = BilinearInterpolationData(*values)
    return bilinear_interpolation(x, y, *corners_data, *values_data)


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
