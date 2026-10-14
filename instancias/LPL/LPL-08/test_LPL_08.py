"""Testes da instancia LPL-08: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
update_server num objeto, mudar a assinatura ou dividir a funcao, desde que
atualize a chamada dentro da unidade; o que nao pode mudar e o conteudo da
tabela de servidores, a mensagem impressa e o erro diante de um valor que o
SQLite nao aceita.

O servidor atualizado e o que tem o mesmo ip (o ip novo e usado tambem no
WHERE). Sem servidor com esse ip, nada muda, mas a mensagem sai do mesmo
jeito; fixado como e.

Cada teste roda numa pasta temporaria, onde fica o frSSH.db.
"""

import sqlite3

import pytest

from LPL_08 import executar

SERVIDOR_1 = ("10.0.0.1", 22, "root", "velha", 1)
SERVIDOR_2 = ("10.0.0.2", 22, "root", "s3nha", 2)


@pytest.fixture(autouse=True)
def _pasta_temporaria(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)


def _tabela():
    conn = sqlite3.connect("frSSH.db")
    linhas = conn.execute("SELECT ip, port, username, password, keyid FROM servers").fetchall()
    conn.close()
    return linhas


def test_tipico_atualiza_so_o_servidor_com_o_mesmo_ip(capsys):
    atualizado = ("10.0.0.1", 2222, "admin", "nova", None)

    linhas = executar([SERVIDOR_1, SERVIDOR_2], atualizado)

    assert linhas == [atualizado, SERVIDOR_2]
    assert capsys.readouterr().out == "Server updated.\n"


def test_borda_ip_sem_cadastro_nao_muda_nada_mas_imprime(capsys):
    linhas = executar([SERVIDOR_1, SERVIDOR_2], ("10.0.0.9", 2222, "admin", "nova", None))

    assert linhas == [SERVIDOR_1, SERVIDOR_2]
    assert capsys.readouterr().out == "Server updated.\n"


def test_invalido_senha_em_dicionario_nao_muda_nada(capsys):
    with pytest.raises(sqlite3.ProgrammingError):
        executar([SERVIDOR_1, SERVIDOR_2], ("10.0.0.1", 2222, "admin", {"senha": "nova"}, None))

    assert capsys.readouterr().out == ""
    assert _tabela() == [SERVIDOR_1, SERVIDOR_2]
