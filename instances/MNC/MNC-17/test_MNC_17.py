"""Tests for instance MNC-17: they pin the observable behavior of run().

Only run() is imported. The refactoring may reorganize the access to the
JSON; what must not change is the printed text (city and first condition, or
the error message when there is no data) and the error on a response without
the weather conditions.
"""

import pytest

from MNC_17 import run


def test_typical_city_and_description(capsys):
    run({"name": "Lisbon", "weather": [{"description": "clear sky"}]})

    assert capsys.readouterr().out == "The weather in Lisbon is clear sky\n"


def test_edge_several_conditions_and_no_data(capsys):
    run({"name": "Recife", "weather": [{"description": "light rain"}, {"description": "mist"}]})
    run(None)

    assert capsys.readouterr().out == (
        "The weather in Recife is light rain\n"
        "Error: Could not get weather\n"
    )


def test_invalid_response_without_conditions(capsys):
    with pytest.raises(IndexError):
        run({"name": "Lisbon", "weather": []})
