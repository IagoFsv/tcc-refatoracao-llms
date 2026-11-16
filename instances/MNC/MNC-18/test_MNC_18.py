"""Tests for instance MNC-18: they pin the observable behavior of run().

Only run() is imported. The map has 2 x 3 x 4 cells. The refactoring may
reorganize the access to the map; what must not change is which cell gets
terrain (only the one at the current position, negative indices counting
from the end, as in Python lists) and the error on a position outside the
map.
"""

import pytest

from MNC_18 import run


def test_typical_only_the_cell_at_the_current_position_gets_terrain():
    assert run(1, 2, 3) == [(1, 2, 3)]


def test_edge_origin_and_negative_indices():
    assert run(0, 0, 0) == [(0, 0, 0)]
    assert run(-1, -1, -1) == [(1, 2, 3)]
    assert run(0, -3, 1) == [(0, 0, 1)]


def test_invalid_position_outside_the_map():
    with pytest.raises(IndexError):
        run(0, 3, 0)
