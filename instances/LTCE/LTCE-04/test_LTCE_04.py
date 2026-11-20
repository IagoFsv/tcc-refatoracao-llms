"""Tests for instance LTCE-04: they pin the observable behavior of run().

Only run() is imported. tabulate is used for real. The refactoring may
replace the conditional expressions with if statements; what must not change
is the text of the table (and of the header in reStructuredText), the list
of changes returned and the error on a malformed line.
"""

import pytest

from LTCE_04 import run

CHANGES = '8f3e2a1c9d 8f3e2a1 2024-03-02 Fix `retry` delay in sensor (#3812)\n\n1b7c44de0f 1b7c44d 2024-02-27 Add hook for queues\n'
BASE = 'https://github.com/apache/airflow/commit/'


def test_typical_markdown_table_and_changes():
    table, changes = run("1.4.0", CHANGES, BASE)

    assert table == "| Commit                                                         | Committed   | Subject                               |\n|:---------------------------------------------------------------|:------------|:--------------------------------------|\n| [8f3e2a1](https://github.com/apache/airflow/commit/8f3e2a1c9d) | 2024-03-02  | `Fix 'retry' delay in sensor (#3812)` |\n| [1b7c44d](https://github.com/apache/airflow/commit/1b7c44de0f) | 2024-02-27  | `Add hook for queues`                 |"
    assert [(c.short_hash, c.date, c.pr) for c in changes] == [
        ("8f3e2a1", "2024-03-02", "3812"),
        ("1b7c44d", "2024-02-27", None),
    ]
    assert changes[0].message_without_backticks == "Fix 'retry' delay in sensor (#3812)"
    assert changes[0].version == "1.4.0"


def test_edge_rst_table_with_header_and_no_changes():
    table, changes = run("1.4.0", CHANGES, BASE, markdown=False)

    assert table == "\n\n1.4.0\n.....\n\nLatest change: 2024-03-02\n\n================================================================  ===========  =======================================\nCommit                                                            Committed    Subject\n================================================================  ===========  =======================================\n`8f3e2a1 <https://github.com/apache/airflow/commit/8f3e2a1c9d>`_  2024-03-02   ``Fix 'retry' delay in sensor (#3812)``\n`1b7c44d <https://github.com/apache/airflow/commit/1b7c44de0f>`_  2024-02-27   ``Add hook for queues``\n================================================================  ===========  ======================================="
    assert len(changes) == 2
    assert run("1.4.0", "", BASE) == ("", [])
    assert run("1.4.0", "\n\n", BASE, markdown=False) == ("", [])


def test_invalid_line_without_subject():
    with pytest.raises(IndexError):
        run("1.4.0", "8f3e2a1c9d 8f3e2a1 2024-03-02", BASE)
