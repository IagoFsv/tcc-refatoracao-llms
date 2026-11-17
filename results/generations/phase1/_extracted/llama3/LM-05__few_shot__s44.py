"""Extraction of weather data from HTML pages into a dictionary.

Public entry point: run(current_html, forecast_html). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

from bs4 import BeautifulSoup


def _parse_current_weather(current: BeautifulSoup) -> dict:
    """Parse current weather data from soup."""
    current_weather = {
        "Time": current.find("p", class_="sub").text,
        "Temp": remove_special_chars(current.find("div", {"class": "display-temp"}).text),
        "Phrase": remove_special_chars(current.find("div", {"class": "phrase"}).text),
    }
    for item in current.find("div", {"class": "current-weather-details"}).find_all("div", class_="detail-item"):
        div = item.find_all("div")
        if len(div) < 2:
            continue
        current_weather[
            remove_special_chars(div[0].text).capitalize()
        ] = remove_special_chars(div[1].text)
    return current_weather


def _parse_day_night_weather(card: BeautifulSoup, weather: dict) -> None:
    """Parse day and night weather data from card."""
    if "day" in card.find("h2").text.lower():
        weather_ = weather["day"]
    else:
        weather_ = weather["night"]
    weather_["Date"] = card.find("span", class_="short-date").text.strip()
    weather_["Temp"] = remove_special_chars(
        card.find("div", {"class": "temperature"}).text.strip().split("°")[0] + "°"
    )
    weather_["Phrase"] = remove_special_chars(
        card.find("div", {"class": "phrase"}).text.strip()
    )
    for item in card.find("div", {"class": "panels"}).find_all("p", class_="panel-item"):
        panel_ = item.text.split("\n")[0].strip()
        value_ = item.find("span").text.strip()
        weather_[remove_special_chars(panel_.replace(value_, ""))] = remove_special_chars(value_)


def _parse_forecast(forecast: BeautifulSoup, weather: dict) -> None:
    """Parse forecast data from forecast."""
    for wr in forecast.find_all("div", {"class": "daily-wrapper"}):
        forecast_ = {}
        date = wr.find("h2", {"class": "date"})
        forecast_["Date"] = (
            date.find("span").text.strip() + " " + date.find_all("span")[1].text.strip()
        )
        temp = wr.find("div", {"class": "temp"})
        forecast_["Temp"] = {
            "min": remove_special_chars(temp.find("span", {"class": "low"}).text.lstrip("/")),
            "max": remove_special_chars(temp.find("span", {"class": "high"}).text),
        }
        forecast_["Precipitation"] = remove_special_chars(
            wr.find("div", {"class": "precip"}).text.strip()
        )
        for item in wr.find("div", {"class": "panels"}).find_all("p", class_="panel-item"):
            panel_ = item.text.split("\n")[0].strip()
            value_ = item.find("span").text.strip()
            forecast_[remove_special_chars(panel_.replace(value_, ""))] = remove_special_chars(value_)
        weather["forecast"].append(forecast_)


def remove_special_chars(ch: str) -> str:
    """Remove special chars from string."""
    for special in ["\\n", "\\t", "\\r"]:
        ch = ch.replace(special, "")

    return ch.strip()


def parse_weather_to_json(current_html: str, forecast_html: str) -> dict:
    """Parse weather data from soup to JSON."""
    current = BeautifulSoup(current_html, "html.parser")
    forecast = BeautifulSoup(forecast_html, "html.parser")
    weather = {
        "current": _parse_current_weather(current),
        "day": {},
        "night": {},
        "forecast": [],
    }
    for card in current.find_all("div", {"class": "half-day-card"}):
        _parse_day_night_weather(card, weather)
    _parse_forecast(forecast, weather)
    return weather


def run(current_html, forecast_html):
    """Reads both pages (current weather and forecast) and returns the dictionary. Public entry point of this unit."""
    return parse_weather_to_json(current_html, forecast_html)
