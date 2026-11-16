"""Tests for instance LPL-06: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
add_server into an object, change the signature or split the function, as
long as it updates the call inside the unit; what must not change is the
content of the servers table, the printed message and the error on a value
that SQLite does not accept.

Each test runs in a temporary folder, where frSSH.db is kept.
"""

import sqlite3

import pytest

from LPL_06 import run

REGISTERED = ("10.0.0.1", 22, "root", "s3cret", 1)


@pytest.fixture(autouse=True)
def _temporary_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)


def _table():
    conn = sqlite3.connect("frSSH.db")
    rows = conn.execute("SELECT ip, port, username, password, keyid FROM servers").fetchall()
    conn.close()
    return rows


def test_typical_stores_a_new_server(capsys):
    new = ("10.0.0.2", 2222, "admin", "other", None)

    rows = run([REGISTERED], new)

    assert rows == [REGISTERED, new]
    assert capsys.readouterr().out == "Server added.\n"


def test_edge_repeated_server_becomes_a_second_row(capsys):
    rows = run([REGISTERED], REGISTERED)

    assert rows == [REGISTERED, REGISTERED]
    assert capsys.readouterr().out == "Server added.\n"


def test_invalid_port_in_a_list_stores_nothing(capsys):
    with pytest.raises(sqlite3.ProgrammingError):
        run([REGISTERED], ("10.0.0.2", [2222], "admin", "other", None))

    assert capsys.readouterr().out == ""
    assert _table() == [REGISTERED]
