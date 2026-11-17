from dataclasses import dataclass, asdict

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Corners:
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

def bilinear_interpolation(point: Point, corners: Corners, values: Values):
    x, y = point
    x1, x2, y1, y2 = corners
    z11, z12, z21, z22 = values
    return (
        z11 * (x2 - x) * (y2 - y)
        + z21 * (x - x1) * (y2 - y)
        + z12 * (x2 - x) * (y - y1)
        + z22 * (x - x1) * (y - y1)
    ) / ((x2 - x1) * (y2 - y1))

def run(point: Point, corners: Corners, values: Values):
    """point: (x, y). corners: (x1, x2, y1, y2). values: (z11, z12, z21, z22). Public entry point of this unit."""
    return bilinear_interpolation(point, corners, values)
