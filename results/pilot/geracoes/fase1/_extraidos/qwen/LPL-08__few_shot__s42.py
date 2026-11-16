import sqlite3
from dataclasses import dataclass, asdict

@dataclass
class Servidor:
    ip: str
    port: int
    username: str
    password: str
    keyid: str

def _preparar_banco(cadastrados):
    conn = sqlite3.connect('frSSH.db')
    conn.execute(f"CREATE TABLE IF NOT EXISTS servers (ip, port, username, password, keyid)")
    conn.executemany(f"INSERT INTO servers VALUES (?, ?, ?, ?, ?)", (asdict(s) for s in cadastrados))
    conn.commit()
    conn.close()


def _linhas():
    conn = sqlite3.connect('frSSH.db')
    linhas = conn.execute("SELECT * FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return linhas


def update_server(servidor: Servidor):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("UPDATE servers SET ip=?, port=?, username=?, password=?, keyid=? WHERE ip=?", 
              (servidor.ip, servidor.port, servidor.username, servidor.password, servidor.keyid, servidor.ip))
    conn.commit()
    conn.close()
    print("Server updated.")


def executar(cadastrados, servidor: Servidor):
    """cadastrados: lista de Servidor."""
    _preparar_banco(cadastrados)
    update_server(servidor)
    return _linhas()
