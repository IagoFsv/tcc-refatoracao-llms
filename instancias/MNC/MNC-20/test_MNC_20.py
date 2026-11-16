"""Tests for instance MNC-20: they pin the observable behavior of run().

Only run() is imported. run receives the map descriptions as
descriptions[x][y][z]. The refactoring may reorganize how the scene is built
and the loops; what must not change is the printed text (100 blank lines to
clear the screen, one line per (x, y) with the z descriptions joined, and a
blank line at the end) and the error on an irregular map.
"""

import pytest

from MNC_20 import run

CLEAR_SCREEN = "\n" * 101  # print("\n" * 100) plus the line break of print itself


def test_typical_one_line_per_x_and_y(capsys):
    run([[["a", "b"], ["c", "d"]],
         [["e", "f"], ["g", "h"]]])

    assert capsys.readouterr().out == CLEAR_SCREEN + "ab\ncd\nef\ngh\n" + "\n"


def test_edge_empty_descriptions_and_one_cell_map(capsys):
    run([[["", "~"], ["#", ""]]])
    assert capsys.readouterr().out == CLEAR_SCREEN + "~\n#\n" + "\n"

    run([[["@"]]])
    assert capsys.readouterr().out == CLEAR_SCREEN + "@\n" + "\n"


def test_invalid_irregular_map():
    with pytest.raises(IndexError):
        run([[["a", "b"], ["c"]]])
