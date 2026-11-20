"""Tests for instance CCC-14: they pin the observable behavior of run().

Only run() is imported. Each entry is stored when the monotonic clock reads
its own time, and the repr is taken when the clock reads now. The
refactoring may change how the repr is built; what must not change is the
text: for each key, the repr of the value cut to 16 characters plus '...'
and the age in whole seconds.
"""

import pytest

from CCC_14 import run


def test_typical_values_and_ages():
    text = run([("a", "short", 100.0), ("b", "a value longer than sixteen", 90.4)], 130.0)

    assert text == "{'a': \"'short'... (age=30s)\", 'b': \"'a value longer ... (age=40s)\"}"


def test_edge_empty_cache_and_age_rounding():
    assert run([], 5) == "{}"
    assert run([(1, 7, 10.0)], 10.6) == "{1: '7... (age=1s)'}"


def test_invalid_time_that_is_not_a_number():
    with pytest.raises(TypeError):
        run([("a", 1, None)], 5)
