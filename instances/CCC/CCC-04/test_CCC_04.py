"""Tests for instance CCC-04: they pin the observable behavior of run().

Only run() is imported. data maps key tuples to value tuples; key_index
holds positions in kdims + vdims. The refactoring may change how the sort key
is built; what must not change is the order of the items, the categorical
order and the errors.
"""

import pytest

from CCC_04 import run

DATA = {(2, "b"): (10,), (1, "c"): (30,), (1, "a"): (20,)}


def test_typical_sort_by_key_and_by_value_dimension():
    assert run(DATA, ["x", "y"], ["v"], [0, 1]) == [((1, "a"), (20,)), ((1, "c"), (30,)), ((2, "b"), (10,))]
    assert run(DATA, ["x", "y"], ["v"], [2]) == [((2, "b"), (10,)), ((1, "a"), (20,)), ((1, "c"), (30,))]


def test_edge_categorical_order_incomparable_keys_and_empty_data():
    assert run(DATA, ["x", ("y", ["c", "b", "a"])], ["v"], [1]) == [
        ((1, "c"), (30,)), ((2, "b"), (10,)), ((1, "a"), (20,))]
    assert run({(None,): (1,), (3,): (2,), (1,): (3,)}, ["x"], ["v"], [0]) == [
        ((None,), (1,)), ((1,), (3,)), ((3,), (2,))]
    assert run({}, ["x"], ["v"], [0]) == []


def test_invalid_duplicated_dimension_and_unknown_category():
    with pytest.raises(ValueError, match="Cannot sort on duplicated dimensions"):
        run(DATA, ["x", "y"], ["v"], [0, 0])
    with pytest.raises(ValueError):
        run(DATA, ["x", ("y", ["a"])], ["v"], [1])
