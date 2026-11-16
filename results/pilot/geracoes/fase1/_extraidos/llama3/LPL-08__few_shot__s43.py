from dataclasses import dataclass, asdict

@dataclass
class Servidor:
    ip: str
    port: int
    username: str
    password: str
    keyid: str

def executar(cadastrados: list, servidor: Servidor):
    _preparar_banco(cadastrados)
    update_server(servidor)
    return _linhas()

def update_server(servidor: Servidor):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("UPDATE servers SET ip=?, port=?, username=?, password=?, keyid=? WHERE ip=?", (servidor.ip, servidor.port, servidor.username, servidor.password, servidor.keyid, servidor.ip))
    conn.commit()
    conn.close()
    print("Server updated.")
