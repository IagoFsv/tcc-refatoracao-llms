"""Tests for instance CCC-07: they pin the observable behavior of run().

Only run() is imported. The refactoring may change how the list of files is
built; what must not change is the address of each file and which files
exist.
"""

import pytest

from CCC_07 import run

BASE = "https://raw.githubusercontent.com/facebookresearch/asset/main/"


def test_typical_simplification_files():
    assert run("asset.valid.simp.3") == BASE + "dataset/asset.valid.simp.3"
    assert run("asset.test.simp.0") == BASE + "dataset/asset.test.simp.0"


def test_edge_first_listed_files_and_last_simplification():
    assert run("human_ratings.csv") == BASE + "human_ratings/human_ratings.csv"
    assert run("asset.valid.orig") == BASE + "dataset/asset.valid.orig"
    assert run("asset.test.simp.9") == BASE + "dataset/asset.test.simp.9"


def test_invalid_file_that_does_not_exist():
    with pytest.raises(KeyError):
        run("asset.valid.simp.10")
    with pytest.raises(KeyError):
        run("asset.train.simp.0")
