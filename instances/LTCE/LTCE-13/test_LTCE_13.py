"""Tests for instance LTCE-13: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the conditional
expressions with if statements; what must not change is the merged dict
(ids, merged counts in order, totals) and the errors on mismatched or
missing input.
"""

import pytest

from LTCE_13 import run


def project(counts, project_id=7, org_id=1):
    return {"project_id": project_id, "org_id": org_id, "transaction_counts": counts,
            "total_num_transactions": None, "total_num_classes": None}


def totals(project_id=7, org_id=1):
    return {"project_id": project_id, "org_id": org_id,
            "total_num_transactions": 120.0, "total_num_classes": 3}


def test_typical_merge_keeps_left_order_and_adds_new_names_from_right():
    left = project([("/home", 50.0), ("/cart", 20.0)])
    right = project([("/cart", 99.0), ("/pay", 5.0)])

    assert run(left, right, totals()) == {
        "org_id": 1, "project_id": 7,
        "transaction_counts": [("/home", 50.0), ("/cart", 20.0), ("/pay", 5.0)],
        "total_num_transactions": 120.0, "total_num_classes": 3,
    }


def test_edge_only_left_and_no_totals():
    counts = [("/home", 50.0)]
    merged = run(project(counts))

    assert merged["transaction_counts"] is counts  # the left list itself
    assert merged["total_num_transactions"] is None
    assert merged["total_num_classes"] is None
    assert run(project([]), project([("/a", 1.0)]))["transaction_counts"] == [("/a", 1.0)]


def test_invalid_missing_or_mismatched_projects():
    with pytest.raises(ValueError, match="no transactions passed to merge"):
        run(None)
    with pytest.raises(ValueError) as error:
        run(project([]), project([], project_id=8))
    assert error.value.args == ("mismatched project transactions", (1, 7), (1, 8))
    with pytest.raises(ValueError) as error:
        run(project([]), None, totals(org_id=2))
    assert error.value.args == ("mismatched projectTransaction and projectTransactionTotals", (1, 7), (2, 7))
    with pytest.raises(AssertionError):
        run(None, project([]))
