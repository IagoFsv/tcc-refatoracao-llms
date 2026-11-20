"""Tests for instance CCC-09: they pin the observable behavior of run().

Only run() is imported. The refactoring may turn the generator into a loop
(a list or a generator function); what must not change is which entry points
are found, in distribution order, and the error when no group is given.
"""

import pytest

from CCC_09 import run

DISTRIBUTIONS = [
    ("alpha", {"console_scripts": {"a": "alpha:main", "b": "alpha:other"}, "plugins": {"p": "alpha.p"}}),
    ("beta", {"console_scripts": {"a": "beta:main"}}),
]


def test_typical_every_entry_point_of_the_group():
    assert run(DISTRIBUTIONS, "console_scripts") == [
        ("alpha", "a", "alpha:main"), ("alpha", "b", "alpha:other"), ("beta", "a", "beta:main")]


def test_edge_filter_by_name_and_unknown_group():
    assert run(DISTRIBUTIONS, "console_scripts", "a") == [("alpha", "a", "alpha:main"), ("beta", "a", "beta:main")]
    assert run(DISTRIBUTIONS, "plugins", "a") == []
    assert run(DISTRIBUTIONS, "gui_scripts") == []


def test_invalid_name_without_a_group():
    with pytest.raises(AttributeError):
        run(DISTRIBUTIONS, None, "a")
