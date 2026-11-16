"""Tests for instance MNC-01: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the chained accesses
with helper functions, intermediate variables or classes; what must not
change is the returned dictionary, the printed JSON and the error on missing
data.

The rank catalog (two ranks, three objectives) is fixed and lives in the
unit. Here only the API response changes, built by _rec and _response.
"""

import json

import pytest

from MNC_01 import run


def _rec(complete, total, progress):
    """An API record with a single objective."""
    return {"objectives": [
        {"complete": complete, "completionValue": total, "progress": progress}
    ]}


def _response(characters, character_records, profile_records,
              profile_variables, character_variables):
    """Builds the API response in the format the unit consumes."""
    return {
        "characters": {"data": characters},
        "characterRecords": {"data": {
            cid: {"records": recs} for cid, recs in character_records.items()
        }},
        "profileRecords": {"data": {"records": profile_records}},
        "profileStringVariables": {"data": {"integerValuesByHash": profile_variables}},
        "characterStringVariables": {"data": {
            cid: {"integerValuesByHash": v} for cid, v in character_variables.items()
        }},
    }


def _typical_data():
    """Two characters; the last one played (2) comes later in the dictionary."""
    return _response(
        characters={
            "a": {"characterId": 1, "dateLastPlayed": "2024-01-10T12:00:00"},
            "b": {"characterId": 2, "dateLastPlayed": "2024-03-05T08:00:00"},
        },
        character_records={
            # Character 1 has everything different: if the unit picks the
            # wrong character, the result changes.
            "1": {"9001": _rec(False, 1, 0), "1001": _rec(False, 10, 2),
                  "1002": _rec(False, 500, 7)},
            "2": {"9001": _rec(True, 1, 1), "1001": _rec(True, 10, 10),
                  "1002": _rec(False, 500, 120)},
        },
        profile_records={"9002": _rec(False, 1, 0), "1003": _rec(False, 3, 1)},
        profile_variables={"111": 120},
        character_variables={"1": {"222": 99}, "2": {"222": 3}},
    )


def test_typical_picks_the_last_character_and_builds_the_ranks(capsys):
    result = run(_typical_data())

    assert result == {
        "9001": {
            "completed": True,
            "record_sets": {
                "501": {
                    "completed": False,
                    "records": {
                        "1001": {"completed": True, "completionValue": 10, "progress": 10},
                        "1002": {"completed": False, "completionValue": 500,
                                 "progress": 120, "variables": {"111": 120}},
                    },
                },
            },
        },
        "9002": {
            "completed": False,
            "record_sets": {
                "502": {
                    "completed": False,
                    "records": {
                        "1003": {"completed": False, "completionValue": 3,
                                 "progress": 1, "variables": {"111": 120, "222": 3}},
                    },
                },
            },
        },
    }
    assert capsys.readouterr().out == json.dumps(result, indent=2) + "\n"


def test_edge_a_single_character_with_everything_complete(capsys):
    data = _response(
        characters={"x": {"characterId": 7, "dateLastPlayed": "2024-01-01T00:00:00"}},
        character_records={
            "7": {"9001": _rec(True, 1, 1), "1001": _rec(True, 10, 10),
                  "1002": _rec(True, 500, 500)},
        },
        profile_records={"9002": _rec(True, 1, 1), "1003": _rec(True, 3, 3)},
        profile_variables={"111": 500},
        character_variables={"7": {"222": 3}},
    )

    result = run(data)

    assert [r["completed"] for r in result.values()] == [True, True]
    assert result["9001"]["record_sets"]["501"]["completed"] is True
    assert result["9002"]["record_sets"]["502"]["completed"] is True
    assert result["9002"]["record_sets"]["502"]["records"]["1003"]["variables"] == {
        "111": 500, "222": 3,
    }
    assert capsys.readouterr().out == json.dumps(result, indent=2) + "\n"


def test_invalid_missing_objective_record():
    data = _typical_data()
    del data["characterRecords"]["data"]["2"]["records"]["1002"]

    with pytest.raises(KeyError):
        run(data)
