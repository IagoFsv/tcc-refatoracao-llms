"""Tests for instance LTCE-09: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the conditional
expressions with if statements; what must not change is the count returned
for each input shape and kind of affine argument, and the error on shapes
with an unsupported number of dimensions.
"""

import pytest

from LTCE_09 import run


def test_typical_with_and_without_affine_weights():
    assert run((2, 3, 4, 4), (3,)) == 96 * 5  # weights present
    assert run((2, 3, 4, 4), None) == 96 * 4  # argument without weights


def test_edge_plain_flag_argument_positions_and_dimension_limits():
    assert run((8, 16), True) == 128 * 5
    assert run((8, 16), False) == 128 * 4
    assert run((1, 2, 3, 4, 5), (2,), input_index=1, affine_index=0) == 120 * 5
    assert run((4, 4), (), input_index=2, affine_index=0) == 16 * 5  # empty shape is not None


def test_invalid_number_of_dimensions():
    with pytest.raises(AssertionError):
        run((10,), (10,))
    with pytest.raises(AssertionError):
        run((1, 1, 1, 1, 1, 1), None)
