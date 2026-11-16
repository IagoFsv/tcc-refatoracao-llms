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
    conn.executemany(f"INSERT INTO servers (ip, port, username, password, keyid) VALUES (?, ?, ?, ?, ?)", (asdict(s) for s in cadastrados))
    conn.commit()
    conn.close()


def _linhas():
    conn = sqlite3.connect('frSSH.db')
    linhas = conn.execute(f"SELECT ip, port, username, password, keyid FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return linhas


def executar(cadastrados, servidor: Servidor):
    """cadastrados: lista de Servidor. servidor: Servidor."""
    _preparar_banco(cadastrados)
    _linhas().append(asdict(servidor))
    return _linhas()
