"""Tests for instance LLF-09: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the lambdas with named
functions, loops or comprehensions, and return lists instead of iterators
(run converts everything into lists before comparing); what must not change
is the content read, with the type of each item, and the error on an item
that is not a number. The comparison uses repr because -2 == -2.0.

The tests pin the behavior as it is: the text is split by comma only at the
first level, and each item comes back converted with float and wrapped in
three single-element lists (the stored structure is not recovered).
"""

import pytest

from LLF_09 import run


def test_typical_each_float_comes_back_in_three_single_element_lists():
    assert repr(run("1.5,-2,3e2")) == "[[[[1.5]]], [[[-2.0]]], [[[300.0]]]]"


def test_edge_spaces_infinity_and_underscore():
    assert repr(run(" 0.25 ,inf,1_0")) == "[[[[0.25]]], [[[inf]]], [[[10.0]]]]"


def test_invalid_item_that_is_not_a_number():
    with pytest.raises(ValueError):
        run("1.5,abc")
