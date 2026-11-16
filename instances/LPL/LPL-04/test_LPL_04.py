"""Tests for instance LPL-04: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
simulate_quicksort, partition and quicksort into an object, change the
signatures or move the functions out, as long as it updates the calls inside
the unit; what must not change is the result, the sequence of frames and the
ticks.

Arithmetic of the typical test, [1, 3, 0, 2]:
  quicksort(0, 3), partition with the pivot at position 3 (value 2), i = -1:
    j = 0: compares 0 and 3 (1 <= 2): i = 0, equal to j, no swap.
    j = 1: compares 1 and 3 (3 > 2): moves on.
    j = 2: compares 2 and 3 (0 <= 2): i = 1, different from j: swaps 1 and
           2, [1, 0, 3, 2].
    end: i + 1 = 2, different from 3: swaps 2 and 3, [1, 0, 2, 3]. Pivot at 2.
  quicksort(0, 1), partition with the pivot at position 1 (value 0), i = -1:
    j = 0: compares 0 and 1 (1 > 0): moves on.
    end: i + 1 = 0, different from 1: swaps 0 and 1, [0, 1, 2, 3]. Pivot at 0.
  quicksort(0, -1), quicksort(1, 1) and quicksort(3, 3) do nothing.
  Comparison: 2 frames (no highlight, with the pair). Swap: 4 frames (no
  highlight, with the pair before, with the pair after, no highlight after).
  Each frame is followed by a tick. 4 comparisons, 3 swaps and the final
  frame: 21 frames and 21 ticks, all with rate 3.
"""

import pytest

from LPL_04 import run


def _f(texts, highlight=()):
    return (tuple(texts), tuple(highlight), 40, 100)


def _compare(texts, i, j):
    return [_f(texts), _f(texts, (i, j))]


def _swap(before, after, i, j):
    return [_f(before), _f(before, (i, j)), _f(after, (i, j)), _f(after)]


def test_typical_four_elements_with_and_without_swaps():
    ordered, frames, ticks = run([1, 3, 0, 2])

    assert ordered == [0, 1, 2, 3]
    assert frames == (
        _compare("1302", 0, 3)
        + _compare("1302", 1, 3)
        + _compare("1302", 2, 3)
        + _swap("1302", "1032", 1, 2)
        + _swap("1032", "1023", 2, 3)
        + _compare("1023", 0, 1)
        + _swap("1023", "0123", 0, 1)
        + [_f("0123")]
    )
    assert ticks == [3] * 21


def test_edge_empty_list_only_draws_the_final_frame():
    ordered, frames, ticks = run([])

    assert ordered == []
    assert frames == [_f("")]
    assert ticks == [3]


def test_invalid_values_that_cannot_be_compared():
    with pytest.raises(TypeError):
        run([3, "a", 1])
