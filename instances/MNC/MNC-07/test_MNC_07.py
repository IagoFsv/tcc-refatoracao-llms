"""Tests for instance MNC-07: they pin the observable behavior of run().

Only run() is imported. The refactoring may give names to the matrices and
the indices; what must not change is the score returned for each board
(weights by sequence length, sequences blocked by the opponent or by a block
do not count, +inf/-inf when someone has already won) and the error on a
nonexistent player.

The expected values come from running the original code.
"""

import pytest

from MNC_07 import run


def test_typical_symmetric_score_for_both_players():
    board = ["XX..",
             ".O..",
             "..X.",
             "O..."]

    assert run(board, 3, "X") == 20
    assert run(board, 3, "O") == -20
    assert run(board, 4, "X") == 12

    in_a_column = ["X...",
                   "X...",
                   "....",
                   "O..."]
    assert run(in_a_column, 3, "X") == 24


def test_edge_empty_board_win_and_block():
    assert run(["....", "....", "....", "...."], 3, "X") == 0

    x_wins = ["XXX.",
              ".O..",
              "O...",
              "...."]
    assert run(x_wins, 3, "X") == float("inf")
    assert run(x_wins, 3, "O") == float("-inf")

    with_block = ["X.*..",
                  ".X...",
                  "..O..",
                  "...O.",
                  "....."]
    assert run(with_block, 3, "X") == -48
    assert run(with_block, 4, "X") == -16

    opponent_and_block_on_the_same_row = ["XO*.",
                                          "....",
                                          "OX*.",
                                          "X..."]
    assert run(opponent_and_block_on_the_same_row, 3, "X") == 28
    assert run(opponent_and_block_on_the_same_row, 3, "O") == -28


def test_invalid_nonexistent_player():
    with pytest.raises(KeyError):
        run(["X..", "...", "..."], 3, "Z")
