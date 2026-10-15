"""Testes da instancia MNC-12: fixam o comportamento observavel de executar().

So executar() e importado. executar roda o arquivo da unidade como programa
(bloco __main__), com a cidade na linha de comando. O teste roda numa pasta
temporaria com o config.ini e intercepta requests.get, que devolve uma
resposta gravada da API de clima. A refatoracao pode reorganizar o bloco
principal (inclusive move-lo para uma funcao chamada sob a mesma guarda); o
que nao pode mudar e a URL consultada, o texto impresso e a saida com codigo
1 diante de cidade invalida.
"""

import pytest
import requests

from MNC_12 import executar

CONFIG = "[openweathermap]\napi_key = chave123\nbase_url = http://api.exemplo.com/weather?\n"


class Resposta:
    def __init__(self, dados):
        self.dados = dados

    def json(self):
        return self.dados


@pytest.fixture
def api(tmp_path, monkeypatch):
    """Pasta com o config.ini e requests.get interceptado; devolve as URLs pedidas."""
    (tmp_path / "config.ini").write_text(CONFIG, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    pedidos = []
    respostas = {}

    def falso_get(url, *args, **kwargs):
        pedidos.append(url)
        return Resposta(respostas["dados"])

    monkeypatch.setattr(requests, "get", falso_get)
    return pedidos, respostas


def clima(*descricoes):
    return {"cod": 200, "weather": [{"description": d} for d in descricoes]}


def test_tipico_imprime_a_descricao_do_clima(api, capsys):
    pedidos, respostas = api
    respostas["dados"] = clima("light rain")

    executar("London")

    assert pedidos == ["http://api.exemplo.com/weather?appid=chave123&q=London"]
    assert capsys.readouterr().out == "light rain\n"


def test_borda_cidade_com_espacos_e_varias_condicoes(api, capsys):
    pedidos, respostas = api
    respostas["dados"] = clima("haze", "mist")

    executar("Rio de Janeiro")

    assert pedidos == ["http://api.exemplo.com/weather?appid=chave123&q=Rio de Janeiro"]
    assert capsys.readouterr().out == "haze\n"  # so a primeira condicao


def test_invalido_cidade_inexistente_sai_com_codigo_1(api, capsys):
    _, respostas = api
    respostas["dados"] = {"cod": "404", "message": "city not found"}

    with pytest.raises(SystemExit) as saida:
        executar("Atlantida")

    assert saida.value.code == 1
    assert capsys.readouterr().out == "Invalid city name\n"
