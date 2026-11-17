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


def _prepare_database(registered: list[Server]):
    conn = sqlite3.connect('frSSH.db')
    conn.execute(f"CREATE TABLE IF NOT EXISTS servers ({_COLUMNS})")
    conn.executemany(f"INSERT INTO servers ({_COLUMNS}) VALUES (?, ?, ?, ?, ?)", [asdict(s) for s in registered])
    conn.commit()
    conn.close()


def _rows():
    conn = sqlite3.connect('frSSH.db')
    rows = conn.execute(f"SELECT {_COLUMNS} FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return rows


def remove_server(server: Server):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("DELETE FROM servers WHERE ip=?", (server.ip,))
    conn.commit()
    conn.close()
    print("Server removed.")


def run(registered: list[Server], server: Server):
    """registered: list of Server objects. Public entry point of this unit."""
    _prepare_database(registered)
    remove_server(server)
    return _rows()
