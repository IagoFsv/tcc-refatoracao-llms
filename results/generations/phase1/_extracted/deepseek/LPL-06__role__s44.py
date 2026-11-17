"""Registry of SSH servers in an SQLite database.

Public entry point: run(registered, server). Do not change its name or
signature; the rest of the file may be freely reorganized.

The database is the file frSSH.db in the current folder. run creates the
servers table, stores the already registered servers, stores a new server and
returns the rows of the table, in insertion order.
"""

import sqlite3

_COLUMNS = "ip, port, username, password, keyid"


class Server:
    def __init__(self, ip, port, username, password, keyid):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.keyid = keyid


class ServerDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('frSSH.db')
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS servers  ({_COLUMNS})")

    def prepare_database(self, registered):
        self.conn.executemany(f"INSERT INTO servers  ({_COLUMNS}) VALUES  (?, ?, ?, ?, ?)", registered)
        self.conn.commit()

    def add_server(self, server):
        c = self.conn.cursor()
        c.execute("INSERT INTO servers  (ip, port, username, password, keyid) VALUES  (?, ?, ?, ?, ?)",
                  (server.ip, server.port, server.username, server.password, server.keyid))
        self.conn.commit()

    def rows(self):
        rows = self.conn.execute(f"SELECT {_COLUMNS} FROM servers ORDER BY rowid").fetchall()
        return rows


def run(registered, server):
    """registered: list of tuples (ip, port, username, password, keyid). Public entry point of this unit."""
    db = ServerDatabase()
    db.prepare_database(registered)
    db.add_server(Server(*server))
    return db.rows()
