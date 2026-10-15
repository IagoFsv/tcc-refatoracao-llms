"""Testes da instancia MNC-16: fixam o comportamento observavel de executar().

So executar() e importado. A refatoracao pode reorganizar o acesso ao JSON e
a montagem das linhas; o que nao pode mudar e o texto impresso (previsao
agrupada por dia nas opcoes -f/-F, clima atual nas demais, unidades de cada
opcao, uma casa decimal) e o erro diante de opcao desconhecida no modo de
clima atual, que acontece depois do cabecalho ja impresso.
"""

import pytest

from MNC_16 import executar

LINHA = "-------------------------------------------------------\n"


def item(dt_txt, temp, tempo):
    return {"dt_txt": dt_txt, "main": {"temp": temp}, "weather": [{"main": tempo}]}


ATUAL = {
    "main": {"temp": 21.25, "feels_like": 20.0, "humidity": 60, "temp_min": 19.96, "temp_max": 23.0},
    "wind": {"speed": 3.06},
    "weather": [{"main": "Clear"}],
}


def test_tipico_previsao_agrupada_por_dia(capsys):
    previsao = {"list": [
        item("2026-10-14 09:00:00", 12.345, "Rain"),
        item("2026-10-14 12:00:00", 15.0, "Clouds"),
        item("2026-10-15 00:00:00", -0.05, "Clear"),
    ]}

    executar(previsao, "Oslo", "-f")

    assert capsys.readouterr().out == (
        "5-day Forecast for Oslo\n"
        + LINHA
        + "Date: 2026-10-14\n"
        "Time: 09:00 Temperature: 12.3°C Weather: Rain\n"
        "Time: 12:00 Temperature: 15.0°C Weather: Clouds\n"
        + LINHA
        + "Date: 2026-10-15\n"
        "Time: 00:00 Temperature: -0.1°C Weather: Clear\n"
    )


def test_borda_clima_atual_imperial_e_previsao_imperial(capsys):
    executar(ATUAL, "Recife", "-C")
    assert capsys.readouterr().out == (
        LINHA
        + "Current Weather for Recife\n"
        "Temperature: 21.2°F\n"
        "Wind Speed: 3.1mph\n"
        "Weather: Clear\n"
        "Feels Like: 20.0°F\n"
        "Humidity: 60%\n"
        "Minimum Temperature: 20.0°F\n"
        "Maximum Temperature: 23.0°F\n"
        + LINHA
    )

    executar({"list": [item("2026-10-14 21:00:00", 70, "Snow")]}, "Boston", "-F")
    assert capsys.readouterr().out == (
        "5-day Forecast for Boston\n"
        + LINHA
        + "Date: 2026-10-14\n"
        "Time: 21:00 Temperature: 70.0°F Weather: Snow\n"
    )


def test_invalido_opcao_desconhecida_no_clima_atual(capsys):
    with pytest.raises(KeyError):
        executar(ATUAL, "Recife", "-x")

    assert capsys.readouterr().out == LINHA + "Current Weather for Recife\n"
