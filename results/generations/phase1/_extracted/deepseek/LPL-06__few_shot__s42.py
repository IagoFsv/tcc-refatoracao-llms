"""Registry of SSH servers in an SQLite database.

Public entry point: run(registered, server). Do not change its name or
signature; the rest of the file may be freely reorganized.

The database is the file frSSH.db in the current folder. run creates the
servers table, stores the already registered servers, stores a new server and
returns the rows of the table, in insertion order.
"""

import sqlite3
from dataclasses import dataclass, asdict

_COLUMNS = "ip, port, username, password, keyid"

@dataclass
class Server:
    ip: str
    port: int
    username: str
    password: str
    keyid: str

def _prepare_database(registered):
    conn = sqlite3.connect('frSSH.db')
    conn.execute(f"CREATE TABLE IF NOT EXISTS servers  ({_COLUMNS})")
    for server in registered:
        conn.execute(f"INSERT INTO servers  ({_COLUMNS}) VALUES  (?, ?, ?, ?, ?)", asdict(server))
    conn.commit()
    conn.close()

def _rows():
    conn = sqlite3.connect('frSSH.db')
    rows = conn.execute(f"SELECT {_COLUMNS} FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return rows

def add_server(server: Server):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("INSERT INTO servers  (ip, port, username, password, keyid) VALUES  (?, ?, ?, ?, ?)", asdict(server))
    conn.commit()
    conn.close()
    print("Server added.")

def run(registered, server):
    """registered: list of Server objects. Public entry point of this unit."""
    registered = [Server(*server) for server in registered]
    _prepare_database(registered)
    add_server(Server(*server))
    return _rows()
