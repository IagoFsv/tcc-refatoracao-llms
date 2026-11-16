"""Tests for instance LPL-07: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
remove_server into an object, drop the unused ones, change the signature or
split the function, as long as it updates the call inside the unit; what
must not change is the content of the servers table, the printed message and
the errors.

Defect of the original, pinned as it is: the DELETE parameters are passed as
(ip), which is the string itself, not a tuple. SQLite treats each character
as a parameter, so a common IP (8 characters for 1 placeholder) raises
ProgrammingError, and only a one-character ip actually removes anything.

Each test runs in a temporary folder, where frSSH.db is kept.
"""

import sqlite3

import pytest

from LPL_07 import run

SERVER_1 = ("10.0.0.1", 22, "root", "s3cret", 1)
SERVER_2 = ("10.0.0.2", 2222, "admin", "other", None)


@pytest.fixture(autouse=True)
def _temporary_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)


def _table():
    conn = sqlite3.connect("frSSH.db")
    rows = conn.execute("SELECT ip, port, username, password, keyid FROM servers").fetchall()
    conn.close()
    return rows


def test_typical_common_ip_raises_and_removes_nothing(capsys):
    with pytest.raises(sqlite3.ProgrammingError):
        run([SERVER_1, SERVER_2], SERVER_1)

    assert capsys.readouterr().out == ""
    assert _table() == [SERVER_1, SERVER_2]


def test_edge_one_character_ip_removes_all_with_that_ip(capsys):
    a1 = ("a", 22, "root", "s3cret", 1)
    b = ("b", 22, "root", "s3cret", 1)
    a2 = ("a", 2222, "admin", "other", None)

    rows = run([a1, b, a2], ("a", 1, "x", "y", 9))

    assert rows == [b]
    assert capsys.readouterr().out == "Server removed.\n"


def test_invalid_ip_none(capsys):
    with pytest.raises(sqlite3.ProgrammingError):
        run([SERVER_1], (None, 22, "root", "s3cret", 1))

    assert capsys.readouterr().out == ""
    assert _table() == [SERVER_1]
