"""Tests for instance LM-06: they pin the observable behavior of run().

Only run() is imported. What is pinned is the printed text, line by line,
with the termcolor colors (the real one, pinned in requirements).

termcolor decides whether to color from the environment (FORCE_COLOR,
NO_COLOR, terminal) and caches the decision; the fixture fixes the
environment and clears the cache. Two parts of the output depend on the
clock: today's date, which the test computes the same way, and the elapsed
time in the footer, checked only by its format.
"""

import re
from datetime import datetime

import pytest
import termcolor

from LM_06 import run


@pytest.fixture
def environment(monkeypatch):
    """Returns a function that turns color on or off for the rest of the test."""
    for name in ("ANSI_COLORS_DISABLED", "NO_COLOR", "FORCE_COLOR", "TERM"):
        monkeypatch.delenv(name, raising=False)

    def with_color(on):
        monkeypatch.setenv("FORCE_COLOR" if on else "NO_COLOR", "1")
        termcolor.can_colorize.cache_clear()

    yield with_color
    termcolor.can_colorize.cache_clear()


def color(text, code, bold=False):
    """Same format as termcolor: color, then bold outside it, and reset."""
    text = f"\033[{code}m{text}"
    return ("\033[1m" + text if bold else text) + "\033[0m"


def _today():
    return datetime.now().strftime("%a, %d-%b-%y")


def _footer(lines, colored):
    """Checks and removes the last two lines (footer with the elapsed time)."""
    assert lines[-2] == ("\033[32m" if colored else "")
    elapsed = r"Powered by AccuWeather \(\d+\.\d+s\)"
    if colored:
        elapsed = re.escape("\033[33m") + elapsed + re.escape("\033[0m" + color("-" * 17, 31) + "\033[0m")
    else:
        elapsed += "-" * 17
    assert re.fullmatch(" " + "-" * 17 + elapsed, lines[-1]), lines[-1]
    return lines[:-2]


def test_typical_complete_data_in_color(environment, capsys):
    """Typical case: partial current and day data, 6 forecast days, with color."""
    environment(True)
    data = {
        "current": {"Time": "10:30 AM", "Temp": "21°C", "Phrase": "Sunny",
                    "Wind": "N 10 km/h", "Humidity": "70%"},
        "day": {"Temp": "24°", "Phrase": "Sunny", "Wind": "N 12 km/h"},
        "night": {},
        "forecast": [{"Date": f"D{i}", "Temp": {"max": f"{20 + i}°", "min": f"{10 + i}°"},
                      "Wind": " S 5", "Rain": f"{i} mm"} for i in range(6)],
    }

    run(data, "são paulo", "br")

    lines = _footer(capsys.readouterr().out.split("\n")[:-1], True)
    forecast = []
    for i in range(1, 6):
        forecast += [color(f" -> D{i} | {20 + i}° >>>>> {10 + i}°", 35),
                     color(f"   - Rain: {i} mm | Hours of Rain: N/A | Cloud Cover: N/A", 32),
                     color("   - Wind: S 5 | Gusts: N/A | Thunder: N/A", 33)]
    assert lines == [
        color(f"[*] Current Weather for São paulo, BR [{color(_today(), 33)}{color(']', 32)}", 32, True),
        color(" - 10:30 AM | Temp: 21°C | Feels: Sunny | AQI (?)", 31),
        color(" - RealFeel Sun: N/A | RealFeel Shade: N/A | UV Index: N/A", 34),
        color(" - Wind:  10 km/h | Gusts: N/A | Cloud Cover: N/A", 32),
        color(" - Dew Point: N/A | Humidity: 70% | Indoor Humidity: N/A", 36),
        color(" - Visibility: N/A | Pressure: N/A | Ceiling: N/A", 33),
        "\033[1m\033[31m", "[*] DayTime Forecast\033[0m",
        color(" - Temp: 24° | Feels: Sunny | AQI (?)", 33),
        color(" - UV Index: N/A | Wind: N 12 km/h | Gusts: N/A", 32),
        color(" - Cloud Cover: N/A | Rain: N/A | Thunder: N/A", 34),
        "\033[1m\033[31m", "[*] NightTime Forecast\033[0m",
        color(" - Temp: N/A | Feels: N/A | AQI (?)", 33),
        color(" - UV Index: N/A | Wind: N/A | Gusts: N/A", 32),
        color(" - Cloud Cover: N/A | Rain: N/A | Thunder: N/A", 34),
        "\033[1m\033[31m", "[*] Forecast for next 5 days\033[0m",
        *forecast,
    ]


def test_edge_empty_data_without_color(environment, capsys):
    """Edge: dictionary with only 6 empty forecasts, without color: everything
    becomes N/A and the first day in the list (index 0) is never printed."""
    environment(False)

    run({"forecast": [{"Date": "ignored"}] + [{}] * 5}, "lisbon", "pt")

    lines = _footer(capsys.readouterr().out.split("\n")[:-1], False)
    na = " - Temp: N/A | Feels: N/A | AQI (?)"
    period = [na, " - UV Index: N/A | Wind: N/A | Gusts: N/A",
              " - Cloud Cover: N/A | Rain: N/A | Thunder: N/A"]
    assert lines == [
        f"[*] Current Weather for Lisbon, PT [{_today()}]",
        " - N/A | Temp: N/A | Feels: N/A | AQI (?)",
        " - RealFeel Sun: N/A | RealFeel Shade: N/A | UV Index: N/A",
        " - Wind: N/A | Gusts: N/A | Cloud Cover: N/A",
        " - Dew Point: N/A | Humidity: N/A | Indoor Humidity: N/A",
        " - Visibility: N/A | Pressure: N/A | Ceiling: N/A",
        "", "[*] DayTime Forecast", *period,
        "", "[*] NightTime Forecast", *period,
        "", "[*] Forecast for next 5 days",
        *[" -> N/A | N/A >>>>> N/A",
          "   - Rain: N/A | Hours of Rain: N/A | Cloud Cover: N/A",
          "   - Wind: N/A | Gusts: N/A | Thunder: N/A"] * 5,
    ]


def test_invalid_forecast_with_fewer_than_six_days(environment, capsys):
    """Invalid: with 3 forecasts, prints days 1 and 2 and fails on the third."""
    environment(False)

    with pytest.raises(IndexError):
        run({"forecast": [{}] * 3}, "lisbon", "pt")

    lines = capsys.readouterr().out.split("\n")[:-1]
    assert lines[-7:] == ["[*] Forecast for next 5 days",
                          *[" -> N/A | N/A >>>>> N/A",
                            "   - Rain: N/A | Hours of Rain: N/A | Cloud Cover: N/A",
                            "   - Wind: N/A | Gusts: N/A | Thunder: N/A"] * 2]
