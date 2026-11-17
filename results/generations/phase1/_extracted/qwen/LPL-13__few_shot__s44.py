from dataclasses import dataclass, asdict

@dataclass
class BilinearData:
    point: tuple
    corners: tuple
    values: tuple

def bilinear_interpolation(data: BilinearData):
    """Bilinear interpolation. It considers the values of the four points
    around the point to be interpolated and returns the interpolated value.
    Made with a lot of help from GitHub Copilot.

    Parameters
    ----------
    data : BilinearData
        Object containing the point, corners, and values to be interpolated.

    Returns
    -------
    float
        Interpolated value.

    Examples
    --------
    >>> from rocketpy.tools import bilinear_interpolation
    >>> bilinear_interpolation(BilinearData((0.5, 0.5), (0, 1, 0, 1), (0, 1, 1, 0)))
    0.5
    """
    x, y = data.point
    x1, x2, y1, y2 = data.corners
    z11, z12, z21, z22 = data.values
    return (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))


def run(data: BilinearData):
    """Public entry point of this unit."""
    return bilinear_interpolation(data)
