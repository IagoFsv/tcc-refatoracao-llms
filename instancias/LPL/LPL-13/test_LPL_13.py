"""Tests for instance LPL-13: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
bilinear_interpolation into objects (point, rectangle, values), change the
signature or split the function, as long as it updates the call inside the
unit; what must not change is the interpolated value and the error on a
degenerate rectangle.

Arithmetic of the typical test: point (1.5, 3) in the rectangle with x from
1 to 3 and y from 2 to 6, values z11=1, z12=2, z21=3, z22=5. The rectangle
does not start at zero, so that x - x1 and x + x1 give different results.
  1*1.5*3 + 3*0.5*3 + 2*1.5*1 + 5*0.5*1 = 4.5 + 4.5 + 3 + 2.5 = 14.5
  14.5 / (2*4) = 1.8125
"""

import pytest

from LPL_13 import run

CORNERS = (1, 3, 2, 6)
VALUES = (1, 2, 3, 5)


def test_typical_asymmetric_point_inside_the_rectangle():
    assert run((1.5, 3), CORNERS, VALUES) == pytest.approx(1.8125)


def test_edge_point_at_a_corner_returns_the_corner_value():
    # (x2, y2) is the corner of z22; (x2, y1) is the corner of z21.
    assert run((3, 6), CORNERS, VALUES) == pytest.approx(5)
    assert run((3, 2), CORNERS, VALUES) == pytest.approx(3)


def test_invalid_rectangle_without_width():
    with pytest.raises(ZeroDivisionError):
        run((2, 3), (2, 2, 2, 6), VALUES)
