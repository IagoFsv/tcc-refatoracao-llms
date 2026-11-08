import sqlite3
from dataclasses import dataclass, asdict

_COLUNAS = "ip, port, username, password, keyid"

@dataclass
class Server:
    ip: str
    port: int
    username: str
    password: str
    keyid: str

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

def add_server(server: Server):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("INSERT INTO servers  (ip, port, username, password, keyid) VALUES  (?, ?, ?, ?, ?)", 
              (server.ip, server.port, server.username, server.password, server.keyid))
    conn.commit()
    conn.close()
    print("Server added.")

def executar(cadastrados, servidor):
    """cadastrados: lista de tuplas (ip, port, username, password, keyid)."""
    _preparar_banco(cadastrados)
    add_server(Server(*servidor))
    return _linhas()
