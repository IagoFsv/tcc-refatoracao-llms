import sqlite3

_COLUNAS = "ip, port, username, password, keyid"


class Server:
    def __init__(self, ip, port, username, password, keyid):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.keyid = keyid


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('frSSH.db')
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS servers  ({_COLUNAS})")

    def prepare(self, cadastrados):
        self.conn.executemany(f"INSERT INTO servers  ({_COLUNAS}) VALUES  (?, ?, ?, ?, ?)", cadastrados)
        self.conn.commit()

    def add_server(self, server):
        c = self.conn.cursor()
        c.execute("INSERT INTO servers  (ip, port, username, password, keyid) VALUES  (?, ?, ?, ?, ?)", 
                  (server.ip, server.port, server.username, server.password, server.keyid))
        self.conn.commit()

    def get_rows(self):
        linhas = self.conn.execute(f"SELECT {_COLUNAS} FROM servers ORDER BY rowid").fetchall()
        return linhas

    def close(self):
        self.conn.close()


def executar(cadastrados, servidor):
    db = Database()
    db.prepare(cadastrados)
    server = Server(*servidor)
    db.add_server(server)
    rows = db.get_rows()
    db.close()
    return rows
