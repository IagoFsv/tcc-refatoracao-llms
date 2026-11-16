"""Tests for instance LLF-08: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the lambdas with named
functions, loops or comprehensions, and return lists instead of iterators
(run converts everything into lists before comparing); what must not change
is the content read, with the type of each item, and the error on an item
that is not an integer. The comparison uses repr because 3 == 3.0 and
1 == True.

The tests pin the behavior as it is: the text is split by comma only at the
first level, and each item comes back converted with int and wrapped in three
single-element lists (the stored structure is not recovered).
"""

import pytest

from LLF_08 import run


def test_typical_each_integer_comes_back_in_three_single_element_lists():
    assert repr(run("3,-1,+7")) == "[[[[3]]], [[[-1]]], [[[7]]]]"


def test_edge_spaces_zero_and_underscore():
    assert repr(run(" 4 ,0,1_000")) == "[[[[4]]], [[[0]]], [[[1000]]]]"


def test_invalid_item_that_is_not_an_integer():
    with pytest.raises(ValueError):
        run("2,3.5")
