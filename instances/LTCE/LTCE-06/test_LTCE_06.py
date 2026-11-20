"""Tests for instance LTCE-06: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the conditional
expression with an if statement; what must not change is the object
returned (the Python override when there is one, otherwise the item itself)
and the errors raised by malformed items.
"""

import pytest

from LTCE_06 import run


def test_typical_python_override_or_the_item_itself():
    python = {"name": "click", "args": ["selector"]}
    with_override = {"name": "click", "langs": {"overrides": {"python": python, "java": {}}}}
    without_override = {"name": "goto", "langs": {"only": ["python"]}}

    assert run(with_override) is python
    assert run(without_override) is without_override


def test_edge_empty_or_missing_python_override_returns_the_item():
    no_python = {"name": "fill", "langs": {"overrides": {"java": {"name": "fill"}}}}
    empty_python = {"name": "type", "langs": {"overrides": {"python": {}}}}
    empty_overrides = {"name": "press", "langs": {"overrides": {}}}

    assert run(no_python) is no_python
    assert run(empty_python) is empty_python
    assert run(empty_overrides) is empty_overrides


def test_invalid_items_without_langs_or_with_overrides_that_are_not_a_dict():
    with pytest.raises(KeyError):
        run({"name": "check"})
    with pytest.raises(AttributeError):
        run({"name": "check", "langs": {"overrides": ["python"]}})
