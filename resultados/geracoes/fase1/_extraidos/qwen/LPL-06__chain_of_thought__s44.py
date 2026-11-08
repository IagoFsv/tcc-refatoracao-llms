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
    conn.executemany(f"INSERT INTO servers ({_COLUNAS}) VALUES (?, ?, ?, ?, ?)", cadastrados)
    conn.commit()
    conn.close()

def _linhas():
    conn = sqlite3.connect('frSSH.db')
    linhas = conn.execute(f"SELECT {_COLUNAS} FROM servers ORDER BY rowid").fetchall()
    conn.close()
    return linhas

def add_server(servidor):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("INSERT INTO servers (ip, port, username, password, keyid) VALUES (?, ?, ?, ?, ?)", 
              (servidor.ip, servidor.port, servidor.username, servidor.password, servidor.keyid))
    conn.commit()
    conn.close()
    print("Server added.")

def executar(cadastrados, servidor):
    """cadastrados: lista de tuplas (ip, port, username, password, keyid)."""
    _preparar_banco(cadastrados)
    add_server(servidor)
    return _linhas()

# Exemplo de uso
if __name__ == "__main__":
    cadastrados = [
        ('192.168.1.1', '22', 'user1', 'pass1', 'key1'),
        ('192.168.1.2', '22', 'user2', 'pass2', 'key2')
    ]
    novo_servidor = Servidor('192.168.1.3', '22', 'user3', 'pass3', 'key3')
    resultado = executar(cadastrados, novo_servidor)
    print(resultado)
