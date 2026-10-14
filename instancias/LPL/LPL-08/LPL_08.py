"""Cadastro de servidores SSH num banco SQLite.

Ponto de entrada publico: executar(cadastrados, servidor). Nao altere o nome
nem a assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.

O banco e o arquivo frSSH.db da pasta atual. executar cria a tabela de
servidores, grava os servidores ja cadastrados, atualiza um servidor e devolve as
linhas da tabela, na ordem de insercao.
"""

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


def update_server(ip, port, username, password, keyid):
    conn = sqlite3.connect('frSSH.db')
    c = conn.cursor()
    c.execute("UPDATE servers SET ip=?, port=?, username=?, password=?, keyid=? WHERE ip=?", (ip, port, username, password, keyid, ip))
    conn.commit()
    conn.close()
    print("Server updated.")


def executar(cadastrados, servidor):
    """cadastrados: lista de tuplas (ip, port, username, password, keyid)."""
    _preparar_banco(cadastrados)
    ip, port, username, password, keyid = servidor
    update_server(ip, port, username, password, keyid)
    return _linhas()
