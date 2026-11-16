"""Tests for instance LLF-07: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the lambdas with named
functions, loops or comprehensions, and return lists instead of iterators
(run converts everything into lists before comparing); what must not change
is the content read and the error on a stored value that is not text.

The tests pin the behavior as it is: the text is split by comma only at the
first level, and each item comes back wrapped in three single-element lists
(the stored structure is not recovered). Spaces are kept and a trailing comma
produces an empty item.
"""

import pytest

from LLF_07 import run


def test_typical_each_item_comes_back_in_three_single_element_lists():
    assert run("sword,shield,potion") == [
        [[["sword"]]],
        [[["shield"]]],
        [[["potion"]]],
    ]


def test_edge_empty_text_spaces_and_trailing_comma():
    assert run("") == [[[[""]]]]
    assert run(" a ,b,") == [[[[" a "]]], [[["b"]]], [[[""]]]]


def test_invalid_stored_value_that_is_not_text():
    with pytest.raises(AttributeError):
        run(42)
