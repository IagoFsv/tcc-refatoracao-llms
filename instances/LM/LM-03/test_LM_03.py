"""Tests for instance LM-03: they pin the observable behavior of run().

Only run() is imported. The function is pure: what is pinned is the
(columns, rows) pair returned for each number of elements, including at the
boundaries between ranges, and the error for what falls in no range.
"""

import pytest

from LM_03 import run


# (first, last, result) of each range of the table, from 1 to 91.
RANGES = [
    (1, 1, (1, 1)), (2, 2, (2, 1)), (3, 3, (3, 1)), (4, 4, (4, 1)), (5, 5, (5, 1)),
    (6, 6, (6, 1)), (7, 8, (4, 2)), (9, 10, (5, 2)), (11, 12, (6, 2)),
    (13, 18, (6, 3)), (19, 24, (6, 4)), (25, 30, (6, 5)), (31, 35, (7, 5)),
    (36, 42, (7, 6)), (43, 49, (7, 7)), (50, 56, (7, 8)), (57, 63, (7, 9)),
    (64, 70, (7, 10)), (71, 77, (7, 11)), (78, 84, (7, 12)), (85, 91, (7, 13)),
]


def test_typical_the_whole_table_from_1_to_91():
    """Typical case: each integer from 1 to 91 falls in its range of the table."""
    for first, last, result in RANGES:
        for elements in range(first, last + 1):
            assert run(elements) == result, elements


def test_edge_range_boundaries_and_golden_ratio():
    """Edge: zero and negatives, range changes and the computation above 91."""
    assert run(-3) == (1, 1)
    assert run(0) == (1, 1)
    assert run(1) == (1, 1)
    assert run(6) == (6, 1)
    assert run(12) == (6, 2)
    assert run(13) == (6, 3)
    assert run(18) == (6, 3)
    assert run(35) == (7, 5)
    assert run(36) == (7, 6)
    assert run(91) == (7, 13)
    assert run(92) == (7, 14)
    assert run(100) == (7, 15)
    assert run(1000) == (24, 42)


def test_invalid_fractional_number_outside_the_ranges():
    """Invalid: 12.5 equals no integer and does not fall in range()."""
    with pytest.raises(ValueError, match="Unsupported number of elements: 12.5"):
        run(12.5)
