"""Tests for instance CCC-13: they pin the observable behavior of run().

Only run() is imported. run loads the module again inside a folder and
returns the include folders found under Cython/Includes, sorted (the order
of os.walk depends on the file system). The refactoring may change how the
folders are collected; what must not change is which folders are kept: the
root itself and every folder holding __init__.pyx or __init__.pxd.
"""

import os

from CCC_13 import run

INCLUDES = os.path.join("Cython", "Includes")


def _tree(root, files):
    for relative in files:
        path = root / "Cython" / "Includes" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("")


def test_typical_folders_with_an_init_declaration(tmp_path):
    _tree(tmp_path, ["libc/__init__.pxd", "numpy/__init__.pyx", "other/stuff.pxd"])

    assert run(str(tmp_path)) == [INCLUDES, os.path.join(INCLUDES, "libc"), os.path.join(INCLUDES, "numpy")]


def test_edge_nested_folders_and_missing_tree(tmp_path):
    _tree(tmp_path, ["libc/sub/__init__.pxd", "other/deep/__init__.pxd", "other/notes.txt"])
    assert run(str(tmp_path)) == [INCLUDES, os.path.join(INCLUDES, "libc", "sub"),
                                  os.path.join(INCLUDES, "other", "deep")]

    empty = tmp_path / "empty"
    empty.mkdir()
    assert run(str(empty)) == []


def test_invalid_includes_path_that_is_a_file_is_ignored(tmp_path):
    (tmp_path / "Cython").mkdir()
    (tmp_path / "Cython" / "Includes").write_text("not a folder")

    assert run(str(tmp_path)) == []
