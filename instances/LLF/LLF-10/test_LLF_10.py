"""Tests for instance LLF-10: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the lambdas with named
functions, loops or comprehensions, and return lists instead of iterators
(run converts everything into lists before comparing); what must not change
is the content read, with the type of each item, and the error on a stored
value that is not text. The comparison uses repr because 1 == True.

The tests pin the behavior as it is, including the defect of the original:
each item goes through bool, so any non-empty text becomes True, even "False"
and "0"; only the empty item becomes False. The text is split by comma only
at the first level, and each item comes back wrapped in three single-element
lists (the stored structure is not recovered).
"""

import pytest

from LLF_10 import run


def test_typical_every_non_empty_text_becomes_true():
    assert repr(run("True,False,0")) == "[[[[True]]], [[[True]]], [[[True]]]]"


def test_edge_empty_text_and_trailing_commas_become_false():
    assert repr(run("")) == "[[[[False]]]]"
    assert repr(run("a,,")) == "[[[[True]]], [[[False]]], [[[False]]]]"


def test_invalid_stored_value_that_is_not_text():
    with pytest.raises(AttributeError):
        run(42)
