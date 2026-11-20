"""Tests for instance LTCE-10: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the conditional
expression with an if statement; what must not change is the pair (left,
right) returned for each combination of arguments and the errors on invalid
padding modes.
"""

import pytest

from LTCE_10 import run


def test_typical_valid_and_same_padding_without_output_padding():
    assert run(3, 2, "valid") == (2, 2)
    assert run(3, 2, "same") == (2, 1)
    assert run(5, 1, "valid") == (4, 4)
    assert run(4, 2, "same") == (2, 2)


def test_edge_stride_larger_than_kernel_dilation_output_padding_and_upper_case():
    assert run(2, 5, "valid") == (1, 4)  # output padding fills up to the stride
    assert run(3, 1, "valid", dilation_rate=2) == (4, 4)  # dilated kernel of size 5
    assert run(3, 2, "valid", output_padding=1) == (2, 3)
    assert run(3, 2, "SAME", output_padding=1) == (2, 1)
    assert run(1, 1, "same") == (0, 0)


def test_invalid_padding_mode():
    with pytest.raises(AssertionError):
        run(3, 2, "full")
    with pytest.raises(AttributeError):
        run(3, 2, None)
