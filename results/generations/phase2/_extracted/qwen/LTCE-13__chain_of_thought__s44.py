"""Merging of transaction counts of the same project.

Public entry point: run(left, right=None, totals=None). Do not change its
name or signature; the rest of the file may be freely reorganized.
"""

from typing import TypedDict, List, Tuple, Optional


class ProjectIdentity(TypedDict, total=True):
    """
    Project identity, used to match projects and also to
    order them
    """

    project_id: int
    org_id: int


class ProjectTransactions(TypedDict, total=True):
    """
    Information about the project transactions
    """

    project_id: int
    org_id: int
    transaction_counts: List[Tuple[str, float]]
    total_num_transactions: Optional[float]
    total_num_classes: Optional[int]


class ProjectTransactionsTotals(TypedDict, total=True):
    project_id: int
    org_id: int
    total_num_transactions: float
    total_num_classes: int


def is_same_project(left: ProjectIdentity | None, right: ProjectIdentity | None) -> bool:
    if left is None or right is None:
        return False

    return left["project_id"] == right["project_id"] and left["org_id"] == right["org_id"]


def is_transaction_in_list(transaction_list: List[Tuple[str, float]], transaction_name: str) -> bool:
    for name, _ in transaction_list:
        if name == transaction_name:
            return True
    return False


def merge_transaction_counts(left_transactions: List[Tuple[str, float]], right_transactions: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
    merged_transactions = left_transactions.copy()
    for transaction_name, count in right_transactions:
        if not is_transaction_in_list(merged_transactions, transaction_name):
            merged_transactions.append((transaction_name, count))
    return merged_transactions


def merge_transactions(
    left: ProjectTransactions,
    right: ProjectTransactions | None,
    totals: ProjectTransactionsTotals | None,
) -> ProjectTransactions:
    if right is None and left is None:
        raise ValueError(
            "no transactions passed to merge",
        )

    if left is not None and right is not None and not is_same_project(left, right):
        raise ValueError(
            "mismatched project transactions",
            (left["org_id"], left["project_id"]),
            (right["org_id"], right["project_id"]),
        )

    if totals is not None and not is_same_project(left, totals):
        raise ValueError(
            "mismatched projectTransaction and projectTransactionTotals",
            (left["org_id"], left["project_id"]),
            (totals["org_id"], totals["project_id"]),
        )

    assert left is not None

    if right is None:
        merged_transactions = left["transaction_counts"]
    else:
        merged_transactions = merge_transaction_counts(left["transaction_counts"], right["transaction_counts"])

    return {
        "org_id": left["org_id"],
        "project_id": left["project_id"],
        "transaction_counts": merged_transactions,
        "total_num_transactions": totals.get("total_num_transactions") if totals is not None else None,
        "total_num_classes": totals.get("total_num_classes") if totals is not None else None,
    }


def run(left, right=None, totals=None):
    """Merges the counts of two pages of the same project. Public entry point of this unit."""
    return merge_transactions(left, right, totals)
