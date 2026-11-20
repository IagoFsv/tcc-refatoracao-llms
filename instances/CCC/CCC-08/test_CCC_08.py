"""Tests for instance CCC-08: they pin the observable behavior of run().

Only run() is imported. The refactoring may change how the list is built;
what must not change is where each element comes from (first source, else
second source, else the next base element) and the assertions on the sizes.
"""

import pytest

from CCC_08 import run


def test_typical_elements_from_both_sources_and_the_base():
    assert run([0, None, None, 1], [None, 1, None, 0], (["a", "b"], ["x", "y"]), ["z"]) == ["a", "y", "z", "b"]


def test_edge_empty_lists_and_only_base():
    assert run([], [], ([], []), []) == []
    assert run([None, None], [None, None], ([], []), ["p", "q"]) == ["p", "q"]


def test_invalid_sizes_that_do_not_match():
    with pytest.raises(AssertionError):
        run([0], [None, None], (["a"], []), [])
    with pytest.raises(AssertionError):
        run([None], [None], ([], []), ["z", "w"])
