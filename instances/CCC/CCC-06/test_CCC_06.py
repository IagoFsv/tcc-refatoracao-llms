"""Tests for instance CCC-06: they pin the observable behavior of run().

Only run() is imported. run restores a node from a saved state and returns
the objects its parents now refer to. The refactoring may change how the
references are rebuilt; what must not change is which parents are kept, that
each one still leads to the same object, and the error for a parent that
cannot be referenced weakly.
"""

import pytest

from CCC_06 import run


class Parent:
    pass


def test_typical_each_parent_leads_to_the_same_object():
    first, second = Parent(), Parent()

    restored = run({"first": first, "second": second})

    assert list(restored) == ["first", "second"]
    assert restored["first"] is first
    assert restored["second"] is second


def test_edge_missing_parents_are_dropped_and_empty_state():
    kept = Parent()
    assert run({"gone": None, "kept": kept, "also_gone": None}) == {"kept": kept}
    assert run({}) == {}


def test_invalid_parent_that_cannot_be_referenced_weakly():
    with pytest.raises(TypeError):
        run({"number": 5})
