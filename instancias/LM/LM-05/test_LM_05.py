"""Testes da instancia LM-05: fixam o comportamento observavel de executar().

So executar() e importado. O que se fixa e o dicionario devolvido para duas
paginas HTML montadas aqui, com a estrutura de classes que o trecho procura.
O BeautifulSoup e o de verdade (beautifulsoup4, fixado no requirements).

Defeito do original, fixado como e: os paineis de cada dia da previsao vem
do ultimo cartao de meio periodo da pagina atual (a variavel do laco
anterior), e nao da propria previsao.
"""

import pytest

from LM_05 import executar


def painel(rotulo, valor):
    return f'<p class="panel-item">{rotulo}<span class="value">{valor}</span></p>'


def meio_periodo(titulo, data, temp, frase, paineis):
    return (f'<div class="half-day-card"><h2>{titulo}</h2><span class="short-date"> {data} </span>'
            f'<div class="temperature"> {temp}°Hi </div><div class="phrase"> {frase} </div>'
            f'<div class="panels">{"".join(paineis)}</div></div>')


def detalhe(*divs):
    return '<div class="detail-item">' + "".join(f"<div>{d}</div>" for d in divs) + "</div>"


def atual(detalhes, cartoes):
    return ('<div class="current-weather-card"><p class="sub">10:30 AM</p>'
            '<div class="display-temp"> 21°C </div><div class="phrase">Sunny\\n</div>'
            f'<div class="current-weather-details">{"".join(detalhes)}</div></div>'
            + "".join(cartoes))


def dia(nome, data, maxima, minima, chuva):
    return (f'<div class="daily-wrapper"><h2 class="date"><span> {nome} </span><span>{data}</span></h2>'
            f'<div class="temp"><span class="high">{maxima}°</span><span class="low">/{minima}°</span></div>'
            f'<div class="precip"> {chuva} </div></div>')


DIA = meio_periodo("Day", "10/21", "24", "Sunny",
                   [painel("Max UV Index", "5 Moderate"), painel("Wind", "N 12 km/h")])
NOITE = meio_periodo("Night", "10/21", "14", "Clear", [painel("Wind", "S 5 km/h")])
DETALHES = [detalhe("RealFeel Sun", "25°"), detalhe("WIND", " N 10 km/h "), detalhe("so rotulo")]


def test_tipico_clima_atual_periodos_e_previsao():
    """Caso tipico: dia, noite e dois dias de previsao."""
    previsao = dia("Wed", "10/22", 25, 14, "20%") + dia("Thu", "10/23", 27, 15, "0%")

    assert executar(atual(DETALHES, [DIA, NOITE]), previsao) == {
        "current": {"Time": "10:30 AM", "Temp": "21°C", "Phrase": "Sunny",
                    "Realfeel sun": "25°", "Wind": "N 10 km/h"},
        "day": {"Date": "10/21", "Temp": "24°", "Phrase": "Sunny",
                "Max UV Index": "5 Moderate", "Wind": "N 12 km/h"},
        "night": {"Date": "10/21", "Temp": "14°", "Phrase": "Clear", "Wind": "S 5 km/h"},
        "forecast": [
            {"Date": "Wed 10/22", "Temp": {"min": "14°", "max": "25°"},
             "Precipitation": "20%", "Wind": "S 5 km/h"},
            {"Date": "Thu 10/23", "Temp": {"min": "15°", "max": "27°"},
             "Precipitation": "0%", "Wind": "S 5 km/h"},
        ],
    }


def test_borda_ordem_dos_cartoes_e_previsao_vazia():
    """Borda: 'Tonight' nao contem 'day' e vai para a noite, 'Today' vai para
    o dia; a previsao pega os paineis do ultimo cartao; sem previsao, lista vazia."""
    noite = meio_periodo("Tonight", "10/21", "13", "Rain", [painel("Rain", "2 mm")])
    hoje = meio_periodo("Today", "10/22", "22", "Cloudy", [painel("Cloud Cover", "80%")])
    pagina = atual([detalhe("Humidity", "70%")], [noite, hoje])

    resultado = executar(pagina, dia("Fri", "10/24", 20, 11, "60%"))
    assert resultado["night"] == {"Date": "10/21", "Temp": "13°", "Phrase": "Rain", "Rain": "2 mm"}
    assert resultado["day"] == {"Date": "10/22", "Temp": "22°", "Phrase": "Cloudy", "Cloud Cover": "80%"}
    assert resultado["current"] == {"Time": "10:30 AM", "Temp": "21°C", "Phrase": "Sunny",
                                    "Humidity": "70%"}
    assert resultado["forecast"] == [{"Date": "Fri 10/24", "Temp": {"min": "11°", "max": "20°"},
                                      "Precipitation": "60%", "Cloud Cover": "80%"}]

    assert executar(pagina, "")["forecast"] == []


def test_invalido_pagina_sem_cartao_de_clima_atual():
    """Invalido: sem o bloco current-weather-card, find devolve None."""
    with pytest.raises(AttributeError):
        executar("<p>pagina fora do ar</p>", "")
