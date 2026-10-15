"""Testes da instancia MNC-17: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode reorganizar o acesso ao JSON;
o que nao pode mudar e o texto impresso (cidade e primeira condicao, ou a
mensagem de erro quando nao ha dados) e o erro diante de resposta sem as
condicoes do tempo.
"""

import pytest

from MNC_17 import executar


def test_tipico_cidade_e_descricao(capsys):
    executar({"name": "Lisbon", "weather": [{"description": "clear sky"}]})

    assert capsys.readouterr().out == "The weather in Lisbon is clear sky\n"


def test_borda_varias_condicoes_e_sem_dados(capsys):
    executar({"name": "Recife", "weather": [{"description": "light rain"}, {"description": "mist"}]})
    executar(None)

    assert capsys.readouterr().out == (
        "The weather in Recife is light rain\n"
        "Error: Could not get weather\n"
    )


def test_invalido_resposta_sem_condicoes(capsys):
    with pytest.raises(IndexError):
        executar({"name": "Lisbon", "weather": []})
