import sqlite3

_COLUNAS = "ip, port, username, password, keyid"

class Servidor:
    def __init__(self, ip, port, username, password, keyid):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.keyid = keyid

def _preparar_banco(cadastrados):
    conn = sqlite3.connect('frSSH.db')
    conn.execute(f"CREATE TABLE IF NOT EXISTS servers ({_COLUNAS})")
    for servidor in cadastrados:
        conn.execute(f"INSERT INTO servers ({_COLUNAS}) VALUES (?, ?, ?, ?, ?)", 
                      (servidor.ip, servidor.port, servidor.username, servidor.password, servidor.keyid))
    conn.commit()
    conn.close()

def _linhas():
    conn = sqlite3.connect('frSSH.db')
    linhas = conn.execute(f"SELECT {_COLUNAS} FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return linhas

def update_server(servidor):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("UPDATE servers SET ip=?, port=?, username=?, password=?, keyid=? WHERE ip=?", 
              (servidor.ip, servidor.port, servidor.username, servidor.password, servidor.keyid, servidor.ip))
    conn.commit()
    conn.close()
    print("Server updated.")

def executar(cadastrados, servidor):
    """cadastrados: lista de Servidor. servidor: Servidor."""
    _preparar_banco(cadastrados)
    update_server(servidor)
    return _linhas()
