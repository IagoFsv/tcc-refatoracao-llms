"""Tests for instance MNC-12: they pin the observable behavior of run().

Only run() is imported. run executes the unit file as a program (__main__
block), with the city on the command line. The test runs in a temporary
folder with config.ini and intercepts requests.get, which returns a recorded
response of the weather API. The refactoring may reorganize the main block
(including moving it into a function called under the same guard); what
must not change is the URL queried, the printed text and the exit with code
1 on an invalid city.
"""

import pytest
import requests

from MNC_12 import run

CONFIG = "[openweathermap]\napi_key = key123\nbase_url = http://api.example.com/weather?\n"


class Response:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


@pytest.fixture
def api(tmp_path, monkeypatch):
    """Folder with config.ini and requests.get intercepted; returns the URLs requested."""
    (tmp_path / "config.ini").write_text(CONFIG, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    requests_made = []
    responses = {}

    def fake_get(url, *args, **kwargs):
        requests_made.append(url)
        return Response(responses["data"])

    monkeypatch.setattr(requests, "get", fake_get)
    return requests_made, responses


def weather(*descriptions):
    return {"cod": 200, "weather": [{"description": d} for d in descriptions]}


def test_typical_prints_the_weather_description(api, capsys):
    requests_made, responses = api
    responses["data"] = weather("light rain")

    run("London")

    assert requests_made == ["http://api.example.com/weather?appid=key123&q=London"]
    assert capsys.readouterr().out == "light rain\n"


def test_edge_city_with_spaces_and_several_conditions(api, capsys):
    requests_made, responses = api
    responses["data"] = weather("haze", "mist")

    run("Rio de Janeiro")

    assert requests_made == ["http://api.example.com/weather?appid=key123&q=Rio de Janeiro"]
    assert capsys.readouterr().out == "haze\n"  # only the first condition


def test_invalid_nonexistent_city_exits_with_code_1(api, capsys):
    _, responses = api
    responses["data"] = {"cod": "404", "message": "city not found"}

    with pytest.raises(SystemExit) as exit_info:
        run("Atlantis")

    assert exit_info.value.code == 1
    assert capsys.readouterr().out == "Invalid city name\n"
