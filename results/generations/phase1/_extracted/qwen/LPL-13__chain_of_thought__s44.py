"""Bilinear interpolation of a point inside a rectangle.

Public entry point: run(point, corners, values). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

class BilinearInterpolationParams:
    def __init__(self, x, y, x1, x2, y1, y2, z11, z12, z21, z22):
        self.x = x
        self.y = y
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z11 = z11
        self.z12 = z12
        self.z21 = z21
        self.z22 = z22

def bilinear_interpolation(params):
    """Bilinear interpolation. It considers the values of the four points
    around the point to be interpolated and returns the interpolated value.
    Made with a lot of help from GitHub Copilot.

    Parameters
    ----------
    params : BilinearInterpolationParams
        Parameters for the bilinear interpolation.

    Returns
    -------
    float
        Interpolated value.

    Examples
    --------
    >>> from rocketpy.tools import bilinear_interpolation
    >>> params = BilinearInterpolationParams(0.5, 0.5, 0, 1, 0, 1, 0, 1, 1, 0)
    >>> bilinear_interpolation(params)
    0.5
    """
    x, y, x1, x2, y1, y2, z11, z12, z21, z22 = (
        params.x, params.y, params.x1, params.x2, params.y1, params.y2,
        params.z11, params.z12, params.z21, params.z22
    )
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
    params = BilinearInterpolationParams(x, y, x1, x2, y1, y2, z11, z12, z21, z22)
    return bilinear_interpolation(params)
