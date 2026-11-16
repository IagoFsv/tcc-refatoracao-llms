"""Tests for instance MNC-19: they pin the observable behavior of run().

Only run() is imported. The map has 2 x 3 x 4 cells. The refactoring may
reorganize the access to the map; what must not change is the returned cell
(negative indices counting from the end, as in Python lists) and the error
on a position outside the map.
"""

import pytest

from MNC_19 import run


def test_typical_cell_at_the_requested_position():
    assert run(1, 2, 3) == (1, 2, 3)
    assert run(0, 1, 2) == (0, 1, 2)


def test_edge_origin_and_negative_indices():
    assert run(0, 0, 0) == (0, 0, 0)
    assert run(-1, -1, -1) == (1, 2, 3)
    assert run(-2, 0, -4) == (0, 0, 0)


def test_invalid_position_outside_the_map():
    with pytest.raises(IndexError):
        run(0, 0, 4)
