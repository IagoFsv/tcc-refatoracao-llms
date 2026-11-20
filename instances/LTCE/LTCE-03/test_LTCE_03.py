"""Tests for instance LTCE-03: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the conditional
expressions with if statements; what must not change is the value returned
(a list with the element), the null value when requested, and the messages
printed and the exit on runtime errors.
"""

import pytest

from LTCE_03 import run


def test_typical_element_of_a_list_and_character_of_a_string():
    assert run([10, 20, 30], 1) == [20]
    assert run("hello", 4) == ["o"]
    assert run([["a", "b"], 7], 0) == [["a", "b"]]


def test_edge_negative_index_and_null_result():
    assert run([10, 20, 30], -1) == [30]  # negative index is not checked
    assert run("hi", -2) == ["h"]
    assert run([10, 20, 30], 0, should_return_null=True) == "\n"


def test_invalid_index_out_of_range_not_a_number_or_not_a_list(capsys):
    with pytest.raises(SystemExit) as error:
        run([10, 20], 2)
    assert error.value.code == "Index Out of Range: 2"
    assert capsys.readouterr().out == "RUNTIME ERROR: index out of range\n"

    with pytest.raises(SystemExit) as error:
        run("abc", "1")
    assert error.value.code == "Index is not a number: 1"
    assert capsys.readouterr().out == "RUNTIME ERROR: index is not a number\n"

    with pytest.raises(SystemExit) as error:
        run(42, 0)
    assert error.value.code == "List is not a list or string: 42"
    assert capsys.readouterr().out == "RUNTIME ERROR: list is not a list or string\n"
