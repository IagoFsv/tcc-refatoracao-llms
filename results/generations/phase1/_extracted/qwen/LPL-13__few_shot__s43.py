from dataclasses import dataclass, asdict

@dataclass
class BilinearInterpolationParams:
    x: float
    y: float
    x1: float
    x2: float
    y1: float
    y2: float
    z11: float
    z12: float
    z21: float
    z22: float

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
    params = BilinearInterpolationParams(x=point[0], y=point[1], x1=corners[0], x2=corners[1], y1=corners[2], y2=corners[3], z11=values[0], z12=values[1], z21=values[2], z22=values[3])
    return bilinear_interpolation(params)
