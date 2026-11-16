"""Tests for instance LM-05: they pin the observable behavior of run().

Only run() is imported. What is pinned is the dictionary returned for two
HTML pages built here, with the class structure the code looks for.
BeautifulSoup is the real one (beautifulsoup4, pinned in requirements).

Defect of the original, pinned as it is: the panels of each forecast day
come from the last half-day card of the current page (the variable of the
previous loop), not from the forecast itself.
"""

import pytest

from LM_05 import run


def panel(label, value):
    return f'<p class="panel-item">{label}<span class="value">{value}</span></p>'


def half_day(title, date, temp, phrase, panels):
    return (f'<div class="half-day-card"><h2>{title}</h2><span class="short-date"> {date} </span>'
            f'<div class="temperature"> {temp}°Hi </div><div class="phrase"> {phrase} </div>'
            f'<div class="panels">{"".join(panels)}</div></div>')


def detail(*divs):
    return '<div class="detail-item">' + "".join(f"<div>{d}</div>" for d in divs) + "</div>"


def current(details, cards):
    return ('<div class="current-weather-card"><p class="sub">10:30 AM</p>'
            '<div class="display-temp"> 21°C </div><div class="phrase">Sunny\\n</div>'
            f'<div class="current-weather-details">{"".join(details)}</div></div>'
            + "".join(cards))


def day(name, date, high, low, rain):
    return (f'<div class="daily-wrapper"><h2 class="date"><span> {name} </span><span>{date}</span></h2>'
            f'<div class="temp"><span class="high">{high}°</span><span class="low">/{low}°</span></div>'
            f'<div class="precip"> {rain} </div></div>')


DAY = half_day("Day", "10/21", "24", "Sunny",
               [panel("Max UV Index", "5 Moderate"), panel("Wind", "N 12 km/h")])
NIGHT = half_day("Night", "10/21", "14", "Clear", [panel("Wind", "S 5 km/h")])
DETAILS = [detail("RealFeel Sun", "25°"), detail("WIND", " N 10 km/h "), detail("label only")]


def test_typical_current_weather_periods_and_forecast():
    """Typical case: day, night and two forecast days."""
    forecast = day("Wed", "10/22", 25, 14, "20%") + day("Thu", "10/23", 27, 15, "0%")

    assert run(current(DETAILS, [DAY, NIGHT]), forecast) == {
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


def test_edge_card_order_and_empty_forecast():
    """Edge: 'Tonight' does not contain 'day' and goes to night, 'Today' goes
    to day; the forecast takes the panels of the last card; without a
    forecast, an empty list."""
    night = half_day("Tonight", "10/21", "13", "Rain", [panel("Rain", "2 mm")])
    today = half_day("Today", "10/22", "22", "Cloudy", [panel("Cloud Cover", "80%")])
    page = current([detail("Humidity", "70%")], [night, today])

    result = run(page, day("Fri", "10/24", 20, 11, "60%"))
    assert result["night"] == {"Date": "10/21", "Temp": "13°", "Phrase": "Rain", "Rain": "2 mm"}
    assert result["day"] == {"Date": "10/22", "Temp": "22°", "Phrase": "Cloudy", "Cloud Cover": "80%"}
    assert result["current"] == {"Time": "10:30 AM", "Temp": "21°C", "Phrase": "Sunny",
                                 "Humidity": "70%"}
    assert result["forecast"] == [{"Date": "Fri 10/24", "Temp": {"min": "11°", "max": "20°"},
                                   "Precipitation": "60%", "Cloud Cover": "80%"}]

    assert run(page, "")["forecast"] == []


def test_invalid_page_without_current_weather_card():
    """Invalid: without the current-weather-card block, find returns None."""
    with pytest.raises(AttributeError):
        run("<p>page is down</p>", "")
