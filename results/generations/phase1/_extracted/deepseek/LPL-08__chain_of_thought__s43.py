import sqlite3

_COLUMNS = "ip, port, username, password, keyid"

class Server:
    def __init__(self, ip, port, username, password, keyid):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.keyid = keyid

class Database:
    def __init__(self, registered):
        self.conn = sqlite3.connect('frSSH.db')
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS servers  ({_COLUMNS})")
        self.conn.executemany(f"INSERT INTO servers  ({_COLUMNS}) VALUES  (?, ?, ?, ?, ?)", registered)
        self.conn.commit()

    def rows(self):
        rows = self.conn.execute(f"SELECT {_COLUMNS} FROM servers ORDER BY rowid").fetchall()
        return rows

    def update_server(self, server):
        c = self.conn.cursor()
        c.execute("UPDATE servers SET ip=?, port=?, username=?, password=?, keyid=? WHERE ip=?", 
                  (server.ip, server.port, server.username, server.password, server.keyid, server.ip))
        self.conn.commit()
        print("Server updated.")

    def close(self):
        self.conn.close()

def run(registered, server):
    """registered: list of tuples  (ip, port, username, password, keyid). Public entry point of this unit."""
    db = Database(registered)
    server = Server(*server)
    db.update_server(server)
    rows = db.rows()
    db.close()
    return rows
