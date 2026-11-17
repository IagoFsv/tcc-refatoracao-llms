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

def bilinear_interpolation(params: BilinearInterpolationParams):
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
    >>> bilinear_interpolation(BilinearInterpolationParams(0.5, 0.5, 0, 1, 0, 1, 0, 1, 1, 0))
    0.5
    """
    return (
        params.z11 * (params.x2 - params.x) * (params.y2 - params.y)
        + params.z21 * (params.x - params.x1) * (params.y2 - params.y)
        + params.z12 * (params.x2 - params.x) * (params.y - params.y1)
        + params.z22 * (params.x - params.x1) * (params.y - params.y1)
    ) / ((params.x2 - params.x1) * (params.y2 - params.y1))


def run(point, corners, values):
    """point: (x, y). corners: (x1, x2, y1, y2). values: (z11, z12, z21, z22). Public entry point of this unit."""
    params = BilinearInterpolationParams(*point, *corners, *values)
    return bilinear_interpolation(params)
