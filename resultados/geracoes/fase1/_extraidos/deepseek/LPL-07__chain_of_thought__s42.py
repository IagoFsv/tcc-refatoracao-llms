import sqlite3

_COLUNAS = "ip, port, username, password, keyid"


def _preparar_banco(cadastrados):
    conn = sqlite3.connect('frSSH.db')
    conn.execute(f"CREATE TABLE IF NOT EXISTS servers ({_COLUNAS})")
    conn.executemany(f"INSERT INTO servers ({_COLUNAS}) VALUES (?, ?, ?, ?, ?)", cadastrados)
    conn.commit()
    conn.close()


def _linhas():
    conn = sqlite3.connect('frSSH.db')
    linhas = conn.execute(f"SELECT {_COLUNAS} FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return linhas


class ServerParameters:
    def __init__(self, ip, port, username, password, keyid):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.keyid = keyid


def remove_server(server_params: ServerParameters):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("DELETE FROM servers WHERE ip=?", (server_params.ip,))
    conn.commit()
    conn.close()
    print("Server removed.")


def executar(cadastrados, server_params: ServerParameters):
    """cadastrados: lista de tuplas (ip, port, username, password, keyid)."""
    _preparar_banco(cadastrados)
    remove_server(server_params)
    return _linhas()
