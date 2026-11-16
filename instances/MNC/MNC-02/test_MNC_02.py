"""Tests for instance MNC-02: they pin the observable behavior of run().

Only run() is imported. The test runs in a temporary folder with the file
tokens/weather.txt and intercepts requests.get, which returns a recorded
response of the weather API. The refactoring may reorganize the access to
the JSON; what must not change is the URL queried, the card sent (title,
color, thumbnail, fields in order, footer) and the error on an error
response from the API.
"""

import pytest
import requests

from MNC_02 import run


class Response:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


def weather_response(temp, city, country):
    return {
        "main": {"temp": temp, "humidity": 72, "pressure": 1012},
        "weather": [{"main": "Clouds", "icon": "04d"}],
        "wind": {"speed": 4.6},
        "clouds": {"all": 75},
        "name": city,
        "sys": {"country": country},
    }


@pytest.fixture
def api(tmp_path, monkeypatch):
    """Folder with the token and requests.get intercepted; returns the URLs requested."""
    (tmp_path / "tokens").mkdir()
    (tmp_path / "tokens" / "weather.txt").write_text("key123", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    requests_made = []
    responses = {}

    def fake_get(url, *args, **kwargs):
        requests_made.append(url)
        return Response(responses["data"])

    monkeypatch.setattr(requests, "get", fake_get)
    return requests_made, responses


def test_typical_card_with_the_weather_data(api):
    requests_made, responses = api
    responses["data"] = weather_response(288.15, "London", "GB")

    sent = run("London")

    assert requests_made == ["https://api.openweathermap.org/data/2.5/weather?q=London&appid=key123"]
    assert len(sent) == 1
    card = sent[0]
    assert card.title == "Weather in London, GB"
    assert card.color == 0x3f3f3f
    assert card.thumbnail == "http://openweathermap.org/img/wn/04d@4x.png"
    assert card.fields == [
        ("Temperature", "15°C", True),
        ("Weather", "Clouds", True),
        ("Wind", "4.6m/s", True),
        ("Humidity", "72%", True),
        ("Pressure", "1012hPa", True),
        ("Cloud Cover", "75%", True),
    ]
    assert card.footer == ("Requested by Ana", "https://cdn.example.com/ana.png")


def test_edge_negative_temperature_rounded(api):
    requests_made, responses = api
    responses["data"] = weather_response(263.0, "Oslo", "NO")  # -10.15 degrees

    card = run("Oslo")[0]

    assert requests_made == ["https://api.openweathermap.org/data/2.5/weather?q=Oslo&appid=key123"]
    assert card.title == "Weather in Oslo, NO"
    assert card.fields[0] == ("Temperature", "-10°C", True)


def test_invalid_error_response_from_the_api(api):
    _, responses = api
    responses["data"] = {"cod": "404", "message": "city not found"}

    with pytest.raises(KeyError):
        run("Atlantis")
