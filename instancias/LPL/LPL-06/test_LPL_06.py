"""Testes da instancia LPL-06: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode agrupar os parametros de
add_server num objeto, mudar a assinatura ou dividir a funcao, desde que
atualize a chamada dentro da unidade; o que nao pode mudar e o conteudo da
tabela de servidores, a mensagem impressa e o erro diante de um valor que o
SQLite nao aceita.

Cada teste roda numa pasta temporaria, onde fica o frSSH.db.
"""

import sqlite3

import pytest

from LPL_06 import executar

CADASTRADO = ("10.0.0.1", 22, "root", "s3nha", 1)


@pytest.fixture(autouse=True)
def _pasta_temporaria(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)


def _tabela():
    conn = sqlite3.connect("frSSH.db")
    linhas = conn.execute("SELECT ip, port, username, password, keyid FROM servers").fetchall()
    conn.close()
    return linhas


def test_tipico_grava_servidor_novo(capsys):
    novo = ("10.0.0.2", 2222, "admin", "outra", None)

    linhas = executar([CADASTRADO], novo)

    assert linhas == [CADASTRADO, novo]
    assert capsys.readouterr().out == "Server added.\n"


def test_borda_servidor_repetido_vira_segunda_linha(capsys):
    linhas = executar([CADASTRADO], CADASTRADO)

    assert linhas == [CADASTRADO, CADASTRADO]
    assert capsys.readouterr().out == "Server added.\n"


def test_invalido_porta_em_lista_nao_grava_nada(capsys):
    with pytest.raises(sqlite3.ProgrammingError):
        executar([CADASTRADO], ("10.0.0.2", [2222], "admin", "outra", None))

    assert capsys.readouterr().out == ""
    assert _tabela() == [CADASTRADO]
