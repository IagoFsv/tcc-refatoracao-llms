"""Tests for instance CCC-12: they pin the observable behavior of run().

Only run() is imported. run loads the module again with extra names in its
namespace and returns the public names. The refactoring may change how the
list of public names is computed; what must not change is which names are
public (not starting with an underscore, not modules, not wantobjects) and
the error for a name that is not a string.
"""

import os

import pytest

from CCC_12 import run

PUBLIC = ["TclError", "TkVersion", "Variable", "getint", "run"]


def test_typical_public_names_of_the_module():
    assert run({}) == PUBLIC


def test_edge_private_names_modules_and_wantobjects_are_left_out():
    assert run({"extra": 1, "_hidden": 2, "helpers": os, "wantobjects": 0}) == sorted(PUBLIC + ["extra"])
    assert run({}) == PUBLIC


def test_invalid_name_that_is_not_a_string():
    with pytest.raises(AttributeError):
        run({1: "x"})
