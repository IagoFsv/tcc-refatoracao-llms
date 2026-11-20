"""Tests for instance LTCE-07: they pin the observable behavior of run().

Only run() is imported. The refactoring may replace the conditional
expressions with if statements; what must not change is the root expression
found and the text rebuilt from the string pieces, including the defect of
the original: the starting piece appears twice in the text.
"""

import pytest

from LTCE_07 import run


def test_typical_concatenation_with_names_in_between():
    assert run("'SELECT * FROM ' + table + ' WHERE id = ' + uid") == ("'SELECT * FROM ' + table + ' WHERE id = ' + uid", ' WHERE id =  SELECT * FROM   WHERE id = ')
    assert run("'a' + 'b'") == ("'a' + 'b'", 'a a b')


def test_edge_single_string_formatting_call_argument_and_non_string_pieces():
    assert run("'only'") == ("'only'", 'only')
    assert run("'user %s' % name") == ("'user %s' % name", 'user %s user %s')
    assert run("run('rm -rf ' + path)") == ("'rm -rf ' + path", 'rm -rf  rm -rf ')
    assert run("'x' + 1 + 'y'") == ("'x' + 1 + 'y'", 'y x y')


def test_invalid_tree_without_parent_links():
    with pytest.raises(AttributeError):
        run("'a' + 'b'", with_parents=False)
