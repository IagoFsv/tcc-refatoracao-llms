import sqlite3

_COLUMNS = "ip, port, username, password, keyid"


class Server:
    def __init__(self, ip, port, username, password, keyid):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.keyid = keyid


def _prepare_database(registered):
    conn = sqlite3.connect('frSSH.db')
    conn.execute(f"CREATE TABLE IF NOT EXISTS servers  ({_COLUMNS})")
    conn.executemany(f"INSERT INTO servers  ({_COLUMNS}) VALUES  (?, ?, ?, ?, ?)", registered)
    conn.commit()
    conn.close()


def _rows():
    conn = sqlite3.connect('frSSH.db')
    rows = conn.execute(f"SELECT  {_COLUMNS} FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return rows


def add_server(server):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("INSERT INTO servers  (ip, port, username, password, keyid) VALUES  (?, ?, ?, ?, ?)", 
              (server.ip, server.port, server.username, server.password, server.keyid))
    conn.commit()
    conn.close()
    print("Server added.")


def run(registered, server):
    """registered: list of tuples (ip, port, username, password, keyid). Public entry point of this unit."""
    _prepare_database(registered)
    add_server(Server(*server))
    return _rows()
