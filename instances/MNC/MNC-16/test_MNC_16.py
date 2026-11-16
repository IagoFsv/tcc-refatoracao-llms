"""Tests for instance MNC-16: they pin the observable behavior of run().

Only run() is imported. The refactoring may reorganize the access to the
JSON and how the lines are built; what must not change is the printed text
(forecast grouped by day with the -f/-F options, current weather with the
others, units of each option, one decimal place) and the error on an unknown
option in current weather mode, which happens after the header has already
been printed.
"""

import pytest

from MNC_16 import run

LINE = "-------------------------------------------------------\n"


def item(dt_txt, temp, weather):
    return {"dt_txt": dt_txt, "main": {"temp": temp}, "weather": [{"main": weather}]}


CURRENT = {
    "main": {"temp": 21.25, "feels_like": 20.0, "humidity": 60, "temp_min": 19.96, "temp_max": 23.0},
    "wind": {"speed": 3.06},
    "weather": [{"main": "Clear"}],
}


def test_typical_forecast_grouped_by_day(capsys):
    forecast = {"list": [
        item("2026-10-14 09:00:00", 12.345, "Rain"),
        item("2026-10-14 12:00:00", 15.0, "Clouds"),
        item("2026-10-15 00:00:00", -0.05, "Clear"),
    ]}

    run(forecast, "Oslo", "-f")

    assert capsys.readouterr().out == (
        "5-day Forecast for Oslo\n"
        + LINE
        + "Date: 2026-10-14\n"
        "Time: 09:00 Temperature: 12.3°C Weather: Rain\n"
        "Time: 12:00 Temperature: 15.0°C Weather: Clouds\n"
        + LINE
        + "Date: 2026-10-15\n"
        "Time: 00:00 Temperature: -0.1°C Weather: Clear\n"
    )


def test_edge_current_weather_imperial_and_forecast_imperial(capsys):
    run(CURRENT, "Recife", "-C")
    assert capsys.readouterr().out == (
        LINE
        + "Current Weather for Recife\n"
        "Temperature: 21.2°F\n"
        "Wind Speed: 3.1mph\n"
        "Weather: Clear\n"
        "Feels Like: 20.0°F\n"
        "Humidity: 60%\n"
        "Minimum Temperature: 20.0°F\n"
        "Maximum Temperature: 23.0°F\n"
        + LINE
    )

    run({"list": [item("2026-10-14 21:00:00", 70, "Snow")]}, "Boston", "-F")
    assert capsys.readouterr().out == (
        "5-day Forecast for Boston\n"
        + LINE
        + "Date: 2026-10-14\n"
        "Time: 21:00 Temperature: 70.0°F Weather: Snow\n"
    )


def test_invalid_unknown_option_in_current_weather(capsys):
    with pytest.raises(KeyError):
        run(CURRENT, "Recife", "-x")

    assert capsys.readouterr().out == LINE + "Current Weather for Recife\n"
