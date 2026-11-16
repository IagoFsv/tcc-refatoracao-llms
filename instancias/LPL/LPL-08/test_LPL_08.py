"""Tests for instance LPL-08: they pin the observable behavior of run().

Only run() is imported. The refactoring may group the parameters of
update_server into an object, change the signature or split the function, as
long as it updates the call inside the unit; what must not change is the
content of the servers table, the printed message and the error on a value
that SQLite does not accept.

The updated server is the one with the same ip (the new ip is also used in
the WHERE). Without a server with that ip, nothing changes, but the message
is printed anyway; pinned as it is.

Each test runs in a temporary folder, where frSSH.db is kept.
"""

import sqlite3

import pytest

from LPL_08 import run

SERVER_1 = ("10.0.0.1", 22, "root", "old", 1)
SERVER_2 = ("10.0.0.2", 22, "root", "s3cret", 2)


@pytest.fixture(autouse=True)
def _temporary_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)


def _table():
    conn = sqlite3.connect("frSSH.db")
    rows = conn.execute("SELECT ip, port, username, password, keyid FROM servers").fetchall()
    conn.close()
    return rows


def test_typical_updates_only_the_server_with_the_same_ip(capsys):
    updated = ("10.0.0.1", 2222, "admin", "new", None)

    rows = run([SERVER_1, SERVER_2], updated)

    assert rows == [updated, SERVER_2]
    assert capsys.readouterr().out == "Server updated.\n"


def test_edge_unregistered_ip_changes_nothing_but_prints(capsys):
    rows = run([SERVER_1, SERVER_2], ("10.0.0.9", 2222, "admin", "new", None))

    assert rows == [SERVER_1, SERVER_2]
    assert capsys.readouterr().out == "Server updated.\n"


def test_invalid_password_in_a_dict_changes_nothing(capsys):
    with pytest.raises(sqlite3.ProgrammingError):
        run([SERVER_1, SERVER_2], ("10.0.0.1", 2222, "admin", {"password": "new"}, None))

    assert capsys.readouterr().out == ""
    assert _table() == [SERVER_1, SERVER_2]
