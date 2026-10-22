"""Testes da instancia LM-06: fixam o comportamento observavel de executar().

So executar() e importado. O que se fixa e o texto impresso, linha a linha,
com as cores do termcolor (o de verdade, fixado no requirements).

O termcolor decide se pinta pelo ambiente (FORCE_COLOR, NO_COLOR, terminal)
e guarda a decisao em cache; a fixture fixa o ambiente e limpa o cache. Duas
partes da saida dependem do relogio: a data de hoje, que o teste calcula do
mesmo jeito, e o tempo decorrido no rodape, conferido so pelo formato.
"""

import re
from datetime import datetime

import pytest
import termcolor

from LM_06 import executar


@pytest.fixture
def ambiente(monkeypatch):
    """Devolve uma funcao que liga ou desliga a cor para o resto do teste."""
    for nome in ("ANSI_COLORS_DISABLED", "NO_COLOR", "FORCE_COLOR", "TERM"):
        monkeypatch.delenv(nome, raising=False)

    def com_cor(ligada):
        monkeypatch.setenv("FORCE_COLOR" if ligada else "NO_COLOR", "1")
        termcolor.can_colorize.cache_clear()

    yield com_cor
    termcolor.can_colorize.cache_clear()


def cor(texto, codigo, negrito=False):
    """Mesmo formato do termcolor: cor, depois negrito por fora, e reset."""
    texto = f"\033[{codigo}m{texto}"
    return ("\033[1m" + texto if negrito else texto) + "\033[0m"


def _hoje():
    return datetime.now().strftime("%a, %d-%b-%y")


def _rodape(linhas, colorido):
    """Confere e tira as duas ultimas linhas (rodape com o tempo decorrido)."""
    assert linhas[-2] == ("\033[32m" if colorido else "")
    tempo = r"Powered by AccuWeather \(\d+\.\d+s\)"
    if colorido:
        tempo = re.escape("\033[33m") + tempo + re.escape("\033[0m" + cor("-" * 17, 31) + "\033[0m")
    else:
        tempo += "-" * 17
    assert re.fullmatch(" " + "-" * 17 + tempo, linhas[-1]), linhas[-1]
    return linhas[:-2]


def test_tipico_dados_completos_em_cores(ambiente, capsys):
    """Caso tipico: dados parciais de agora e do dia, 6 dias de previsao, com cor."""
    ambiente(True)
    dados = {
        "current": {"Time": "10:30 AM", "Temp": "21°C", "Phrase": "Sunny",
                    "Wind": "N 10 km/h", "Humidity": "70%"},
        "day": {"Temp": "24°", "Phrase": "Sunny", "Wind": "N 12 km/h"},
        "night": {},
        "forecast": [{"Date": f"D{i}", "Temp": {"max": f"{20 + i}°", "min": f"{10 + i}°"},
                      "Wind": " S 5", "Rain": f"{i} mm"} for i in range(6)],
    }

    executar(dados, "são paulo", "br")

    linhas = _rodape(capsys.readouterr().out.split("\n")[:-1], True)
    previsao = []
    for i in range(1, 6):
        previsao += [cor(f" -> D{i} | {20 + i}° >>>>> {10 + i}°", 35),
                     cor(f"   - Rain: {i} mm | Hours of Rain: N/A | Cloud Cover: N/A", 32),
                     cor("   - Wind: S 5 | Gusts: N/A | Thunder: N/A", 33)]
    assert linhas == [
        cor(f"[*] Current Weather for São paulo, BR [{cor(_hoje(), 33)}{cor(']', 32)}", 32, True),
        cor(" - 10:30 AM | Temp: 21°C | Feels: Sunny | AQI (?)", 31),
        cor(" - RealFeel Sun: N/A | RealFeel Shade: N/A | UV Index: N/A", 34),
        cor(" - Wind:  10 km/h | Gusts: N/A | Cloud Cover: N/A", 32),
        cor(" - Dew Point: N/A | Humidity: 70% | Indoor Humidity: N/A", 36),
        cor(" - Visibility: N/A | Pressure: N/A | Ceiling: N/A", 33),
        "\033[1m\033[31m", "[*] DayTime Forecast\033[0m",
        cor(" - Temp: 24° | Feels: Sunny | AQI (?)", 33),
        cor(" - UV Index: N/A | Wind: N 12 km/h | Gusts: N/A", 32),
        cor(" - Cloud Cover: N/A | Rain: N/A | Thunder: N/A", 34),
        "\033[1m\033[31m", "[*] NightTime Forecast\033[0m",
        cor(" - Temp: N/A | Feels: N/A | AQI (?)", 33),
        cor(" - UV Index: N/A | Wind: N/A | Gusts: N/A", 32),
        cor(" - Cloud Cover: N/A | Rain: N/A | Thunder: N/A", 34),
        "\033[1m\033[31m", "[*] Forecast for next 5 days\033[0m",
        *previsao,
    ]


def test_borda_dados_vazios_sem_cor(ambiente, capsys):
    """Borda: dicionario so com 6 previsoes vazias, sem cor: tudo vira N/A e o
    primeiro dia da lista (indice 0) nunca e impresso."""
    ambiente(False)

    executar({"forecast": [{"Date": "ignorado"}] + [{}] * 5}, "lisboa", "pt")

    linhas = _rodape(capsys.readouterr().out.split("\n")[:-1], False)
    na = " - Temp: N/A | Feels: N/A | AQI (?)"
    periodo = [na, " - UV Index: N/A | Wind: N/A | Gusts: N/A",
               " - Cloud Cover: N/A | Rain: N/A | Thunder: N/A"]
    assert linhas == [
        f"[*] Current Weather for Lisboa, PT [{_hoje()}]",
        " - N/A | Temp: N/A | Feels: N/A | AQI (?)",
        " - RealFeel Sun: N/A | RealFeel Shade: N/A | UV Index: N/A",
        " - Wind: N/A | Gusts: N/A | Cloud Cover: N/A",
        " - Dew Point: N/A | Humidity: N/A | Indoor Humidity: N/A",
        " - Visibility: N/A | Pressure: N/A | Ceiling: N/A",
        "", "[*] DayTime Forecast", *periodo,
        "", "[*] NightTime Forecast", *periodo,
        "", "[*] Forecast for next 5 days",
        *[" -> N/A | N/A >>>>> N/A",
          "   - Rain: N/A | Hours of Rain: N/A | Cloud Cover: N/A",
          "   - Wind: N/A | Gusts: N/A | Thunder: N/A"] * 5,
    ]


def test_invalido_previsao_com_menos_de_seis_dias(ambiente, capsys):
    """Invalido: com 3 previsoes, imprime os dias 1 e 2 e falha no terceiro."""
    ambiente(False)

    with pytest.raises(IndexError):
        executar({"forecast": [{}] * 3}, "lisboa", "pt")

    linhas = capsys.readouterr().out.split("\n")[:-1]
    assert linhas[-7:] == ["[*] Forecast for next 5 days",
                           *[" -> N/A | N/A >>>>> N/A",
                             "   - Rain: N/A | Hours of Rain: N/A | Cloud Cover: N/A",
                             "   - Wind: N/A | Gusts: N/A | Thunder: N/A"] * 2]
