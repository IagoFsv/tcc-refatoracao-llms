"""Tests for instance LTCE-12: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the conditional
expressions with if statements; what must not change is the name returned
for each combination of class, parent logger name and explicit class logger
name.
"""

import pytest

from LTCE_12 import run


class Task:
    pass


Task.__module__ = "jobs.tasks"


def test_typical_module_and_class_name_with_and_without_parent():
    assert run(Task) == "jobs.tasks.Task"
    assert run(Task, "airflow.task") == "airflow.task.jobs.tasks.Task"
    assert run(Task, None, "custom") == "custom"
    assert run(Task, "airflow.task", "custom") == "airflow.task.custom"


def test_edge_empty_names():
    assert run(Task, "", "custom") == "custom"  # empty parent is ignored
    assert run(Task, "airflow.task", "") == "airflow.task"  # empty class name: only the parent
    assert run(Task, None, "") == ""


def test_invalid_object_without_module_or_name():
    with pytest.raises(AttributeError):
        run(42)
