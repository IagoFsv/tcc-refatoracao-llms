"""Tests for instance LTCE-08: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the conditional
expressions with if statements; what must not change is the content of the
rules built (dicts become objects with the same fields, objects already
built are kept) and the error on fields of the wrong type.
"""

import pytest

from LTCE_08 import run

RULE = {
    "id": "R1",
    "team_id": "T9",
    "title": "Block external sharing",
    "action": {"resolution": {"value": "restrict"}, "notify": [{"entity_type": "admin"}]},
    "condition": {"datatype": "string", "operator": "in", "entity_type": "channel",
                  "values": [{"field": "type", "values": ["public"], "operator": "="}]},
}


def test_typical_dicts_become_objects_and_built_objects_are_reused():
    first, second = run(RULE)

    assert (first.id, first.team_id, first.title) == ("R1", "T9", "Block external sharing")
    assert first.action.resolution.value == "restrict"
    assert [n.entity_type for n in first.action.notify] == ["admin"]
    assert (first.condition.datatype, first.condition.operator, first.condition.entity_type) == ("string", "in", "channel")
    value = first.condition.values[0]
    assert (value.field, value.values, value.operator, value.datatype) == ("type", ["public"], "=", None)
    assert second.action is first.action
    assert second.condition is first.condition


def test_edge_missing_parts_and_unknown_keys():
    first, second = run({"id": "R2", "unknown": 1, "action": {"extra": True}, "condition": {}})

    assert (first.team_id, first.title) == (None, None)
    assert (first.action.resolution, first.action.notify) == (None, None)
    assert (first.condition.values, first.condition.datatype) == (None, None)
    bare, _ = run({})
    assert (bare.id, bare.action, bare.condition) == (None, None, None)


def test_invalid_fields_of_the_wrong_type():
    with pytest.raises(TypeError):
        run({"id": "R3", "action": ["restrict"]})
    with pytest.raises(TypeError):
        run({"id": "R3", "condition": "public"})
