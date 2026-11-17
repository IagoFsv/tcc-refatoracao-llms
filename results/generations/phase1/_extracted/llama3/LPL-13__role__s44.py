"""Bilinear interpolation of a point inside a rectangle.

Public entry point: run(point, corners, values). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""


class BilinearInterpolationParameters:
    def __init__(self, x1, x2, y1, y2, z11, z12, z21, z22):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z11 = z11
        self.z12 = z12
        self.z21 = z21
        self.z22 = z22


def bilinear_interpolation(x, y, params):
    """Bilinear interpolation. It considers the values of the four points
    around the point to be interpolated and returns the interpolated value.
    Made with a lot of help from GitHub Copilot.

    Parameters
    ----------
    x : float
        x coordinate to which the value will be interpolated.
    y : float
        y coordinate to which the value will be interpolated.
    params : BilinearInterpolationParameters
        Parameters for the interpolation.

    Returns
    -------
    float
        Interpolated value.

    Examples
    --------
    >>> from rocketpy.tools import bilinear_interpolation
    >>> params = BilinearInterpolationParameters(0, 1, 0, 1, 0, 1, 1, 0)
    >>> bilinear_interpolation(0.5, 0.5, params)
    0.5
    """
    return (
        params.z11 * (params.x2 - x) * (params.y2 - y)
        + params.z21 * (x - params.x1) * (params.y2 - y)
        + params.z12 * (params.x2 - x) * (y - params.y1)
        + params.z22 * (x - params.x1) * (y - params.y1)
    ) / ((params.x2 - params.x1) * (params.y2 - params.y1))


def run(point, corners, values):
    """point: (x, y). corners: (x1, x2, y1, y2). values: (z11, z12, z21, z22). Public entry point of this unit."""
    x, y = point
    params = BilinearInterpolationParameters(*corners, *values)
    return bilinear_interpolation(x, y, params)
