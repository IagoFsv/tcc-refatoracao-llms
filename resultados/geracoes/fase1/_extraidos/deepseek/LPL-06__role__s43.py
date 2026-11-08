import sqlite3

_COLUNAS = "ip, port, username, password, keyid"

class Server:
    def __init__(self, ip, port, username, password, keyid):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.keyid = keyid

def _preparar_banco(cadastrados):
    conn = sqlite3.connect('frSSH.db')
    conn.execute(f"CREATE TABLE IF NOT EXISTS servers  ({_COLUNAS})")
    conn.executemany(f"INSERT INTO servers  ({_COLUNAS}) VALUES  (?, ?, ?, ?, ?)", cadastrados)
    conn.commit()
    conn.close()

def _linhas():
    conn = sqlite3.connect('frSSH.db')
    linhas = conn.execute(f"SELECT {_COLUNAS} FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return linhas

def add_server(server):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("INSERT INTO servers  (ip, port, username, password, keyid) VALUES  (?, ?, ?, ?, ?)", (server.ip, server.port, server.username, server.password, server.keyid))
    conn.commit()
    conn.close()
    print("Server added.")

def executar(cadastrados, servidor):
    _preparar_banco(cadastrados)
    server = Server(*servidor)
    add_server(server)
    return _linhas()
