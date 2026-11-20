"""Tests for instance CCC-10: they pin the observable behavior of run().

Only run() is imported. The refactoring may change how the fields are
filtered; what must not change is the text: the type name and, in order, the
fields whose value is truthy or equal to 0, leaving out a fixed list of
names.
"""

import pytest

from CCC_10 import run


def test_typical_record_with_a_field_left_out_by_name():
    assert run("WorkerRead", {"source": "src", "output_coders": ["c"]}) == "WorkerRead(source=src)"


def test_edge_zero_false_empty_and_none_values():
    text = run("WorkerDo", {"count": 0, "flag": False, "empty": [], "none": None, "label": "",
                            "window_fn": "w", "serialized_fn": "f", "context": "c", "items": (1, 2)})

    assert text == "WorkerDo(count=0, flag=False, items=(1, 2))"
    assert run("WorkerEmpty", {}) == "WorkerEmpty()"


def test_invalid_field_name_that_is_not_an_identifier():
    with pytest.raises(ValueError):
        run("WorkerBad", {"not valid": 1})
