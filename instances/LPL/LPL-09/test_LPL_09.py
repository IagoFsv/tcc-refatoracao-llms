"""Tests for instance LPL-09: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the coordinates of
draw_line into an object, change the signature or split the method, as long
as it updates the call inside the unit; what must not change are the pixels
marked in the returned image and the error on a point outside the image.

Expected pixels: the ones skimage.draw.line (scikit-image 0.26.0) returns.
"""

import numpy as np
import pytest

from LPL_09 import run


def _expected(size, pixels):
    image = np.zeros(size)
    for row, column in pixels:
        image[row, column] = 1
    return image


def test_typical_sloped_segment():
    image = run((3, 5), (0, 0, 2, 4))

    pixels = [(0, 0), (1, 1), (1, 2), (2, 3), (2, 4)]
    assert np.array_equal(image, _expected((3, 5), pixels))


def test_edge_single_point_segment():
    image = run((5, 5), (2, 3, 2, 3))

    assert np.array_equal(image, _expected((5, 5), [(2, 3)]))


def test_invalid_point_outside_the_image():
    with pytest.raises(IndexError):
        run((5, 5), (0, 0, 0, 9))
