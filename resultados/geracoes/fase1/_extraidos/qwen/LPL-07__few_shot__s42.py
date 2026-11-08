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
    linhas = conn.execute("SELECT ip, port, username, password, keyid FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return linhas


def remove_server(servidor: Servidor):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("DELETE FROM servers WHERE ip=?", (servidor.ip,))
    conn.commit()
    conn.close()
    print("Server removed.")


def executar(cadastrados, servidor: Servidor):
    """cadastrados: lista de Servidor. servidor: Servidor."""
    _preparar_banco(cadastrados)
    remove_server(servidor)
    return _linhas()
