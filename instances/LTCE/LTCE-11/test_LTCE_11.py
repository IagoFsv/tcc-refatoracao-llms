"""Tests for instance LTCE-11: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the conditional
expression with an if statement; what must not change is which errors are
accepted, the value returned, the messages of the assertion errors and the
errors that propagate.
"""

import pytest

from LTCE_11 import run


def test_typical_single_type_with_and_without_match():
    assert run(ValueError, error=ValueError("bad value")) is False  # no pattern: not matched
    assert run(ValueError, match="bad", error=ValueError("bad value")) is True
    assert run([TypeError, ValueError], match="bad", error=TypeError("bad type")) is True


def test_edge_list_of_patterns_tuple_of_types_and_may_pass():
    assert run((KeyError, ValueError), match=["nothing", "^bad"], error=ValueError("bad")) is True
    assert run(ValueError, may_pass=True) is False
    with pytest.raises(AssertionError, match=r"^Did not raise: \[<class 'ValueError'>\]$"):
        run(ValueError)
    with pytest.raises(AssertionError, match=r"^Did not raise: \(<class 'KeyError'>,\)$"):
        run((KeyError,))


def test_invalid_unexpected_error_or_message():
    with pytest.raises(KeyError):
        run(ValueError, error=KeyError("other"))
    with pytest.raises(AssertionError, match="^custom$"):
        run(ValueError, error=KeyError("other"), err_msg="custom")
    with pytest.raises(AssertionError, match="should contain one of the following patterns"):
        run(ValueError, match="good", error=ValueError("bad value"))
