"""Tests for instance LLF-02: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the lambdas with named
functions, loops or comprehensions; what must not change is the text stored
in the configuration, the message logged after storing it, and the error on
an item that is not text.

The tests pin the behavior as it is: the four levels become a flat
comma-separated list (the structure is lost), an empty level leaves an extra
comma, and text at the last level is split letter by letter.
"""

import logging

import pytest

from LLF_02 import run


def test_typical_four_levels_become_comma_separated_text(caplog):
    caplog.set_level(logging.INFO)
    value = [
        [[["a", "b"], ["c"]], [["d"]]],
        [[["e", "f"]]],
    ]

    assert run(value) == "a,b,c,d,e,f"
    assert caplog.messages == ["Config: {'world': {'regions': 'a,b,c,d,e,f'}}"]


def test_edge_text_at_last_level_empty_levels_and_tuples(caplog):
    caplog.set_level(logging.INFO)

    assert run([[["xy", ""]], [[]], []]) == "x,y,,,"  # "xy" comes out letter by letter
    assert run([]) == ""
    assert run((((("pa",),),),)) == "pa"
    assert caplog.messages[0] == "Config: {'world': {'regions': 'x,y,,,'}}"


def test_invalid_item_that_is_not_text():
    with pytest.raises(TypeError):
        run([[[[1, 2]]]])
