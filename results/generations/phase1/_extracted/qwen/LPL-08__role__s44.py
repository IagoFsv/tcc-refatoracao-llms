"""Registry of SSH servers in an SQLite database.

Public entry point: run(registered, server). Do not change its name or
signature; the rest of the file may be freely reorganized.

The database is the file frSSH.db in the current folder. run creates the
servers table, stores the already registered servers, updates a server and
returns the rows of the table, in insertion order.
"""

import sqlite3

class ServerInfo:
    def __init__(self, ip, port, username, password, keyid):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.keyid = keyid

_COLUMNS = "ip, port, username, password, keyid"


def _prepare_database(registered):
    conn = sqlite3.connect('frSSH.db')
    conn.execute(f"CREATE TABLE IF NOT EXISTS servers ({_COLUMNS})")
    conn.executemany(f"INSERT INTO servers ({_COLUMNS}) VALUES (?, ?, ?, ?, ?)", registered)
    conn.commit()
    conn.close()


def _rows():
    conn = sqlite3.connect('frSSH.db')
    rows = conn.execute(f"SELECT {_COLUMNS} FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return rows


def update_server(server_info):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("UPDATE servers SET ip=?, port=?, username=?, password=?, keyid=? WHERE ip=?", 
              (server_info.ip, server_info.port, server_info.username, server_info.password, server_info.keyid, server_info.ip))
    conn.commit()
    conn.close()
    print("Server updated.")


def run(registered, server_info):
    """registered: list of tuples (ip, port, username, password, keyid). Public entry point of this unit."""
    _prepare_database(registered)
    update_server(server_info)
    return _rows()
