"""Tests for instance LLF-04: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the lambdas with named
functions, loops or comprehensions; what must not change is the text stored
in the configuration, the message logged after storing it, and the error on
a last level that is not a sequence.

The tests pin the behavior as it is: the four levels become a flat
comma-separated list (the structure is lost), any item at the last level is
converted with str (int, float, bool, None), an empty level leaves an extra
comma, and text at the last level is split letter by letter.
"""

import logging

import pytest

from LLF_04 import run


def test_typical_numbers_in_four_levels_become_text(caplog):
    caplog.set_level(logging.INFO)
    value = [
        [[[1, 2.5], [3]], [[-4]]],
        [[[0.1, 6]]],
    ]

    assert run(value) == "1,2.5,3,-4,0.1,6"
    assert caplog.messages == ["Config: {'world': {'regions': '1,2.5,3,-4,0.1,6'}}"]


def test_edge_text_bool_none_and_empty_levels(caplog):
    caplog.set_level(logging.INFO)

    assert run([[["12", [True, None]]], [[]]]) == "1,2,True,None,"  # "12" comes out digit by digit
    assert run([]) == ""
    assert run(((((7,),),),)) == "7"
    assert caplog.messages[0] == "Config: {'world': {'regions': '1,2,True,None,'}}"


def test_invalid_last_level_that_is_not_a_sequence():
    with pytest.raises(TypeError):
        run([[[1, 2]]])
