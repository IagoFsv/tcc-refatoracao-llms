import sqlite3

class Servidor:
    def __init__(self, ip, port, username, password, keyid):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.keyid = keyid

def _preparar_banco(cadastrados):
    conn = sqlite3.connect('frSSH.db')
    conn.execute(f"CREATE TABLE IF NOT EXISTS servers (ip, port, username, password, keyid)")
    conn.executemany(f"INSERT INTO servers (ip, port, username, password, keyid) VALUES (?, ?, ?, ?, ?)", 
                      [(s.ip, s.port, s.username, s.password, s.keyid) for s in cadastrados])
    conn.commit()
    conn.close()


def _linhas():
    conn = sqlite3.connect('frSSH.db')
    linhas = conn.execute(f"SELECT ip, port, username, password, keyid FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return linhas


def remove_server(servidor):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("DELETE FROM servers WHERE ip=?", (servidor.ip,))
    conn.commit()
    conn.close()
    print("Server removed.")


def executar(cadastrados, servidor):
    """cadastrados: lista de objetos Servidor. servidor: objeto Servidor."""
    _preparar_banco(cadastrados)
    remove_server(servidor)
    return _linhas()
