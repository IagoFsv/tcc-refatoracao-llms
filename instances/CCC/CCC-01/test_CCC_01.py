"""Tests for instance CCC-01: they pin the observable behavior of run().

Only run() is imported. run returns the coordinates of every cell, grouped
by x and then by y. The refactoring may change how the grid is built; what
must not change is the shape of the grid and the coordinates of each cell.
"""

import pytest

from CCC_01 import run


def test_typical_grid_of_two_by_two_by_three():
    assert run(2, 2, 3) == [
        [[(0, 0, 0), (0, 0, 1), (0, 0, 2)], [(0, 1, 0), (0, 1, 1), (0, 1, 2)]],
        [[(1, 0, 0), (1, 0, 1), (1, 0, 2)], [(1, 1, 0), (1, 1, 1), (1, 1, 2)]],
    ]


def test_edge_single_cell_and_empty_axes():
    assert run(1, 1, 1) == [[[(0, 0, 0)]]]
    assert run(0, 3, 3) == []
    assert run(2, 0, 3) == [[], []]
    assert run(1, 2, 0) == [[[], []]]


def test_invalid_size_that_is_not_an_integer():
    with pytest.raises(TypeError):
        run(2, "2", 2)
