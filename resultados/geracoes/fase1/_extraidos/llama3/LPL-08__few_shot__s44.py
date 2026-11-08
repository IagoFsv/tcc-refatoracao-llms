from dataclasses import dataclass

@dataclass
class Servidor:
    ip: str
    port: int
    username: str
    password: str
    keyid: str

def preparar_banco(cadastrados):
    conn = sqlite3.connect('frSSH.db')
    conn.execute(f"CREATE TABLE IF NOT EXISTS servers ({_COLUNAS})")
    conn.executemany(f"INSERT INTO servers ({_COLUNAS}) VALUES (?, ?, ?, ?, ?)", [(s.ip, s.port, s.username, s.password, s.keyid) for s in cadastrados])
    conn.commit()
    conn.close()

def linhas():
    conn = sqlite3.connect('frSSH.db')
    linhas = conn.execute(f"SELECT {_COLUNAS} FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return linhas

def update_server(servidor):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("UPDATE servers SET ip=?, port=?, username=?, password=?, keyid=? WHERE ip=?", (servidor.ip, servidor.port, servidor.username, servidor.password, servidor.keyid, servidor.ip))
    conn.commit()
    conn.close()
    print("Server updated.")

def executar(cadastrados, servidor: Servidor):
    preparar_banco(cadastrados)
    update_server(servidor)
    return linhas()
