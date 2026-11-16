"""Tests for instance LPL-03: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
simulate_heapsort and heapify into an object, change the signatures or move
heapify out, as long as it updates the calls inside the unit; what must not
change is the result, the sequence of animation frames and the ticks.

Arithmetic of the typical test, [2, 3, 1] (n = 3):
  heap building, i from 3 to 0: only i = 0 has children.
    compares 0 and 1 (2 <= 3, the largest becomes 1), compares 1 and 2
    (3 > 1, stays 1), compares 0 and 1 again before swapping; swap: [3, 2, 1].
  extraction, i = 2: swaps 2 and 0: [1, 2, 3]. heapify(n=2, 0): compares 0
    and 1 (1 <= 2), compares 0 and 1 again, swaps: [2, 1, 3].
  extraction, i = 1: swaps 1 and 0: [1, 2, 3]. heapify(n=1, 0) compares
    nothing.
  Each comparison draws 2 frames (no highlight, then with the pair
  highlighted), with a tick after each; at the end, 1 frame and 1 tick.
  5 comparisons: 11 frames and 11 ticks, all with rate 3.
"""

import pytest

from LPL_03 import run


def _f(texts, highlight=()):
    return (tuple(texts), tuple(highlight), 40, 100)


def test_typical_three_elements_out_of_order():
    ordered, frames, ticks = run([2, 3, 1])

    assert ordered == [1, 2, 3]
    assert frames == [
        _f("231"), _f("231", (0, 1)),
        _f("231"), _f("231", (1, 2)),
        _f("231"), _f("231", (0, 1)),
        _f("123"), _f("123", (0, 1)),
        _f("123"), _f("123", (0, 1)),
        _f("123"),
    ]
    assert ticks == [3] * 11


def test_edge_empty_list_only_draws_the_final_frame():
    ordered, frames, ticks = run([])

    assert ordered == []
    assert frames == [_f("")]
    assert ticks == [3]


def test_invalid_values_that_cannot_be_compared():
    with pytest.raises(TypeError):
        run([3, "a", 1])
