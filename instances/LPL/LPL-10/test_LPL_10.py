"""Tests for instance LPL-10: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the coordinates and the
color of draw_line into an object, change the signature or split the method,
as long as it updates the call inside the unit; what must not change are the
pixels painted in the returned image, the default color (black) and the error
on a color with the wrong number of channels.

Expected pixels: the ones skimage.draw.line (scikit-image 0.26.0) returns.
"""

import numpy as np
import pytest

from LPL_10 import run

SEGMENT = (0, 0, 2, 4)
PIXELS = [(0, 0), (1, 1), (1, 2), (2, 3), (2, 4)]


def _expected(size, pixels, color):
    image = np.full((*size, 3), 255, dtype=np.uint8)
    for row, column in pixels:
        image[row, column] = color
    return image


def test_typical_red_segment():
    image = run((3, 5), SEGMENT, (255, 0, 0))

    assert np.array_equal(image, _expected((3, 5), PIXELS, (255, 0, 0)))


def test_edge_no_color_paints_black():
    image = run((3, 5), SEGMENT)

    assert np.array_equal(image, _expected((3, 5), PIXELS, (0, 0, 0)))


def test_invalid_color_with_two_channels():
    with pytest.raises(ValueError):
        run((3, 5), SEGMENT, (255, 0))
