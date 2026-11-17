"""Registry of SSH servers in an SQLite database.

Public entry point: run(registered, server). Do not change its name or
signature; the rest of the file may be freely reorganized.

The database is the file frSSH.db in the current folder. run creates the
servers table, stores the already registered servers, removes a server and
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

class ServerDB:
    def __init__(self, registered):
        self.conn = sqlite3.connect('frSSH.db')
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS servers  ({_COLUMNS})")
        self.conn.executemany(f"INSERT INTO servers  ({_COLUMNS}) VALUES  (?, ?, ?, ?, ?)", registered)
        self.conn.commit()

    def rows(self):
        rows = self.conn.execute(f"SELECT {_COLUMNS} FROM servers ORDER BY rowid").fetchall()
        return rows

    def remove_server(self, server: Server):
        c = self.conn.cursor()
        c.execute("DELETE FROM servers WHERE ip=?", (server.ip,))
        self.conn.commit()
        print("Server removed.")

    def close(self):
        self.conn.close()

def run(registered, server):
    """registered: list of tuples (ip, port, username, password, keyid). Public entry point of this unit."""
    server_db = ServerDB(registered)
    server = Server(*server)
    server_db.remove_server(server)
    rows = server_db.rows()
    server_db.close()
    return rows
