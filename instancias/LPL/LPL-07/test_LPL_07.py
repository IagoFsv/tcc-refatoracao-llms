"""Testes da instancia LPL-07: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
remove_server num objeto, tirar os que nao sao usados, mudar a assinatura ou
dividir a funcao, desde que atualize a chamada dentro da unidade; o que nao
pode mudar e o conteudo da tabela de servidores, a mensagem impressa e os
erros.

Defeito do original, fixado como e: os parametros do DELETE sao passados
como (ip), que e a propria string, nao uma tupla. O SQLite trata cada
caractere como um parametro, entao um IP comum (8 caracteres para 1
marcador) levanta ProgrammingError, e so um ip de um caractere remove de
fato.

Cada teste roda numa pasta temporaria, onde fica o frSSH.db.
"""

import sqlite3

import pytest

from LPL_07 import executar

SERVIDOR_1 = ("10.0.0.1", 22, "root", "s3nha", 1)
SERVIDOR_2 = ("10.0.0.2", 2222, "admin", "outra", None)


@pytest.fixture(autouse=True)
def _pasta_temporaria(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)


def _tabela():
    conn = sqlite3.connect("frSSH.db")
    linhas = conn.execute("SELECT ip, port, username, password, keyid FROM servers").fetchall()
    conn.close()
    return linhas


def test_tipico_ip_comum_levanta_erro_e_nao_remove(capsys):
    with pytest.raises(sqlite3.ProgrammingError):
        executar([SERVIDOR_1, SERVIDOR_2], SERVIDOR_1)

    assert capsys.readouterr().out == ""
    assert _tabela() == [SERVIDOR_1, SERVIDOR_2]


def test_borda_ip_de_um_caractere_remove_todos_com_esse_ip(capsys):
    a1 = ("a", 22, "root", "s3nha", 1)
    b = ("b", 22, "root", "s3nha", 1)
    a2 = ("a", 2222, "admin", "outra", None)

    linhas = executar([a1, b, a2], ("a", 1, "x", "y", 9))

    assert linhas == [b]
    assert capsys.readouterr().out == "Server removed.\n"


def test_invalido_ip_none(capsys):
    with pytest.raises(sqlite3.ProgrammingError):
        executar([SERVIDOR_1], (None, 22, "root", "s3nha", 1))

    assert capsys.readouterr().out == ""
    assert _tabela() == [SERVIDOR_1]
