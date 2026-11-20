"""Tests for instance CCC-11: they pin the observable behavior of run().

Only run() is imported. The refactoring may change how the list is built;
what must not change is which names are kept (ending in .py, not ending in
_test.py, not excluded), their order and the absolute paths.
"""

import os

import pytest

from CCC_11 import run


def _make(folder, names):
    for name in names:
        (folder / name).write_text("")


def test_typical_scripts_sorted_with_absolute_paths(tmp_path):
    _make(tmp_path, ["b.py", "a.py", "notes.txt"])

    assert run(str(tmp_path)) == [os.path.join(str(tmp_path), "a.py"), os.path.join(str(tmp_path), "b.py")]


def test_edge_test_files_excluded_names_and_empty_folder(tmp_path):
    _make(tmp_path, ["a.py", "a_test.py", "skip.py", "test_b.py"])
    (tmp_path / "pkg.py").mkdir()
    expected = [os.path.join(str(tmp_path), name) for name in ["a.py", "pkg.py", "test_b.py"]]

    assert run(str(tmp_path), {"skip.py"}) == expected
    empty = tmp_path / "empty"
    empty.mkdir()
    assert run(str(empty)) == []


def test_invalid_folder_that_does_not_exist(tmp_path):
    with pytest.raises(FileNotFoundError):
        run(str(tmp_path / "missing"))
