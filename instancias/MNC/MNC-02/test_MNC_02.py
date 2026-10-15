"""Testes da instancia MNC-02: fixam o comportamento observavel de executar().

So executar() e importado. O teste roda numa pasta temporaria com o arquivo
tokens/weather.txt e intercepta requests.get, que devolve uma resposta
gravada da API de clima. A refatoracao pode reorganizar o acesso ao JSON;
o que nao pode mudar e a URL consultada, o cartao enviado (titulo, cor,
miniatura, campos na ordem, rodape) e o erro diante de resposta de erro da API.
"""

import pytest
import requests

from MNC_02 import executar


class Resposta:
    def __init__(self, dados):
        self.dados = dados

    def json(self):
        return self.dados


def resposta_clima(temp, cidade, pais):
    return {
        "main": {"temp": temp, "humidity": 72, "pressure": 1012},
        "weather": [{"main": "Clouds", "icon": "04d"}],
        "wind": {"speed": 4.6},
        "clouds": {"all": 75},
        "name": cidade,
        "sys": {"country": pais},
    }


@pytest.fixture
def api(tmp_path, monkeypatch):
    """Pasta com o token e requests.get interceptado; devolve as URLs pedidas."""
    (tmp_path / "tokens").mkdir()
    (tmp_path / "tokens" / "weather.txt").write_text("chave123", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    pedidos = []
    respostas = {}

    def falso_get(url, *args, **kwargs):
        pedidos.append(url)
        return Resposta(respostas["dados"])

    monkeypatch.setattr(requests, "get", falso_get)
    return pedidos, respostas


def test_tipico_cartao_com_os_dados_do_clima(api):
    pedidos, respostas = api
    respostas["dados"] = resposta_clima(288.15, "London", "GB")

    enviados = executar("London")

    assert pedidos == ["https://api.openweathermap.org/data/2.5/weather?q=London&appid=chave123"]
    assert len(enviados) == 1
    cartao = enviados[0]
    assert cartao.title == "Weather in London, GB"
    assert cartao.color == 0x3f3f3f
    assert cartao.thumbnail == "http://openweathermap.org/img/wn/04d@4x.png"
    assert cartao.fields == [
        ("Temperature", "15°C", True),
        ("Weather", "Clouds", True),
        ("Wind", "4.6m/s", True),
        ("Humidity", "72%", True),
        ("Pressure", "1012hPa", True),
        ("Cloud Cover", "75%", True),
    ]
    assert cartao.footer == ("Requested by Ana", "https://cdn.exemplo.com/ana.png")


def test_borda_temperatura_negativa_arredondada(api):
    pedidos, respostas = api
    respostas["dados"] = resposta_clima(263.0, "Oslo", "NO")  # -10.15 graus

    cartao = executar("Oslo")[0]

    assert pedidos == ["https://api.openweathermap.org/data/2.5/weather?q=Oslo&appid=chave123"]
    assert cartao.title == "Weather in Oslo, NO"
    assert cartao.fields[0] == ("Temperature", "-10°C", True)


def test_invalido_resposta_de_erro_da_api(api):
    _, respostas = api
    respostas["dados"] = {"cod": "404", "message": "city not found"}

    with pytest.raises(KeyError):
        executar("Atlantida")
