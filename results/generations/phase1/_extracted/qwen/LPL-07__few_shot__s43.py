"""Registry of SSH servers in an SQLite database.

Public entry point: run(registered, server). Do not change its name or
signature; the rest of the file may be freely reorganized.

The database is the file frSSH.db in the current folder. run creates the
servers table, stores the already registered servers, removes a server and
returns the rows of the table, in insertion order.
"""

import sqlite3
from dataclasses import dataclass, asdict

@dataclass
class Server:
    ip: str
    port: int
    username: str
    password: str
    keyid: str

def _prepare_database(registered):
    conn = sqlite3.connect('frSSH.db')
    conn.execute(f"CREATE TABLE IF NOT EXISTS servers (ip, port, username, password, keyid)")
    conn.executemany("INSERT INTO servers VALUES (?, ?, ?, ?, ?)", [(s.ip, s.port, s.username, s.password, s.keyid) for s in registered])
    conn.commit()
    conn.close()


def _rows():
    conn = sqlite3.connect('frSSH.db')
    rows = conn.execute("SELECT ip, port, username, password, keyid FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return rows


def remove_server(server: Server):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("DELETE FROM servers WHERE ip=?", (server.ip,))
    conn.commit()
    conn.close()
    print("Server removed.")


def run(registered, server):
    """registered: list of Server. Public entry point of this unit."""
    _prepare_database(registered)
    remove_server(server)
    return _rows()
