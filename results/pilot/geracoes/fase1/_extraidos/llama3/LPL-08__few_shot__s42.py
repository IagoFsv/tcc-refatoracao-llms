from dataclasses import dataclass, asdict

@dataclass
class Server:
    ip: str
    port: int
    username: str
    password: str
    keyid: str

def _preparar_banco(servers: list[Server]):
    conn = sqlite3.connect('frSSH.db')
    conn.execute(f"CREATE TABLE IF NOT EXISTS servers ({_COLUNAS})")
    conn.executemany(f"INSERT INTO servers ({_COLUNAS}) VALUES (?, ?, ?, ?, ?)", [(s.ip, s.port, s.username, s.password, s.keyid) for s in servers])
    conn.commit()
    conn.close()

def _linhas():
    conn = sqlite3.connect('frSSH.db')
    linhas = conn.execute(f"SELECT {_COLUNAS} FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return linhas

def update_server(server: Server):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("UPDATE servers SET ip=?, port=?, username=?, password=?, keyid=? WHERE ip=?", (server.ip, server.port, server.username, server.password, server.keyid, server.ip))
    conn.commit()
    conn.close()
    print("Server updated.")

def executar(servers: list[Server], servidor: Server):
    _preparar_banco(servers)
    update_server(servidor)
    return _linhas()
