"""Tests for instance LTCE-02: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the conditional
expressions with if statements, and the lambdas with named functions, loops
or vectorized methods; what must not change is the list of
cities returned, one per description, in the same order, and the error on a
description that is too short.

The tests pin the behavior as it is, including the defect of the original: a
two-word city ("Abu Dhabi") is never found.
"""

import pytest

from LTCE_02 import run

CITIES = ["Dubai", "Sharjah", "Abu Dhabi", "London"]


def test_typical_last_word_second_to_last_or_unknown():
    descriptions = [
        "Lulu Hypermarket Dubai",       # last word is a city
        "Starbucks Sharjah AE",         # only the second-to-last is a city
        "Netflix Subscription Online",  # neither
        "Transfer London Dubai",        # both: the last one wins
    ]

    assert run(descriptions, CITIES) == ["Dubai", "Sharjah", "Unknown", "Dubai"]


def test_edge_uppercase_two_word_city_and_one_word_description():
    descriptions = [
        "AMAZON LONDON",              # all uppercase
        "payment dubai",              # all lowercase
        "Emirates Palace Abu Dhabi",  # two-word city: never found
        "Dubai",                      # a single word, but a city: no error
    ]
    cities = ["DUBAI", "london", "Abu Dhabi"]  # list with mixed case

    assert run(descriptions, cities) == ["London", "Dubai", "Unknown", "Dubai"]


def test_invalid_one_word_description_that_is_not_a_city():
    with pytest.raises(IndexError):
        run(["Lulu Hypermarket Dubai", "Netflix"], CITIES)
