"""Tests for instance LPL-11: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the center, the radius and
the color of draw_circle into an object, change the signature or split the
method, as long as it updates the call inside the unit; what must not change
are the pixels painted in the returned image, the default color (black), the
clipping at the border and the error on a color with the wrong number of
channels.

The center is given as (x, y): x is the column, y is the row. Expected
pixels: the ones skimage.draw.disk (scikit-image 0.26.0) returns; with radius
2, the disk is the 3x3 square around the center.
"""

import numpy as np
import pytest

from LPL_11 import run


def _expected(size, pixels, color):
    image = np.full((*size, 3), 255, dtype=np.uint8)
    for row, column in pixels:
        image[row, column] = color
    return image


def test_typical_blue_disk_in_the_middle():
    image = run((7, 7), (4, 2, 2), (0, 0, 255))

    pixels = [(r, c) for r in (1, 2, 3) for c in (3, 4, 5)]
    assert np.array_equal(image, _expected((7, 7), pixels, (0, 0, 255)))


def test_edge_disk_clipped_at_the_corner_no_color_paints_black():
    image = run((4, 5), (1, 0, 2))

    pixels = [(r, c) for r in (0, 1) for c in (0, 1, 2)]
    assert np.array_equal(image, _expected((4, 5), pixels, (0, 0, 0)))


def test_invalid_color_with_two_channels():
    with pytest.raises(ValueError):
        run((7, 7), (4, 2, 2), (0, 255))
