"""Extraction of weather data from HTML pages into a dictionary.

Public entry point: run(current_html, forecast_html). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

from bs4 import BeautifulSoup


def parse_weather_to_json(soup: BeautifulSoup, fcast: BeautifulSoup)  -> dict:
    """Parse weather data from soup to JSON."""
    weather = {
        "current": {},
        "day": {},
        "night": {},
        "forecast": [],
    }

    # Get current weather data
    _parse_current_weather(soup, weather)

    # Get day and night weather data
    _parse_day_and_night_weather(soup, weather)

    # get forecast data
    _parse_forecast_data(fcast, weather)

    return weather


def _parse_current_weather(soup: BeautifulSoup, weather: dict):
    current = soup.find("div", {"class": "current-weather-card"})
    weather["current"]["Time"] = _get_text(current, "p", "sub")
    weather["current"]["Temp"] = _remove_special_chars(_get_text(current, "div", "display-temp"))
    weather["current"]["Phrase"] = _remove_special_chars(_get_text(current, "div", "phrase"))
    _parse_current_details(current, weather["current"])


def _parse_day_and_night_weather(soup: BeautifulSoup, weather: dict):
    for card in soup.find_all("div", {"class": "half-day-card"}):
        weather_ = weather["day"] if "day" in card.find("h2").text.lower() else weather["night"]
        weather_["Date"] = _get_text(card, "span", "short-date").strip()
        weather_["Temp"] = _remove_special_chars(_get_text(card, "div", "temperature").strip().split("°")[0] + "°")
        weather_["Phrase"] = _remove_special_chars(_get_text(card, "div", "phrase").strip())
        _parse_weather_details(card, weather_)


def _parse_forecast_data(fcast: BeautifulSoup, weather: dict):
    for wr in fcast.find_all("div", {"class": "daily-wrapper"}):
        forecast = _parse_forecast(wr)
        weather["forecast"].append(forecast)


def _parse_current_details(current: BeautifulSoup, weather: dict):
    for item in current.find("div", {"class": "current-weather-details"}).find_all("div", class_="detail-item"):
        div = item.find_all("div")
        if len(div) < 2:
            continue
        weather[_remove_special_chars(div[0].text).capitalize()] = _remove_special_chars(div[1].text)


def _parse_weather_details(card: BeautifulSoup, weather: dict):
    for item in card.find("div", {"class": "panels"}).find_all("p", class_="panel-item"):
        panel = _remove_special_chars(item.text.split("\n")[0].strip())
        value = _remove_special_chars(item.find("span").text.strip())
        weather[_remove_special_chars(panel.replace(value, ""))] = value


def _parse_forecast(wr: BeautifulSoup) -> dict:
    forecast = {}
    date = wr.find("h2", {"class": "date"})
    forecast["Date"] = _get_text(date, "span") + " " + _get_text(date, "span", None, 1)
    forecast["Temp"] = _parse_temp(wr.find("div", {"class": "temp"}))
    forecast["Precipitation"] = _remove_special_chars(_get_text(wr, "div", "precip").strip())
    _parse_forecast_details(wr, forecast)
    return forecast


def _parse_temp(temp: BeautifulSoup) -> dict:
    return {
        "min": _remove_special_chars(temp.find("span", {"class": "low"}).text.lstrip("/")),
        "max": _remove_special_chars(temp.find("span", {"class": "high"}).text),
    }


def _parse_forecast_details(wr: BeautifulSoup, forecast: dict):
    for item in wr.find("div", {"class": "panels"}).find_all("p", class_="panel-item"):
        panel = _remove_special_chars(item.text.split("\n")[0].strip())
        value = _remove_special_chars(item.find("span").text.strip())
        forecast[_remove_special_chars(panel.replace(value, ""))] = value


def _get_text(element: BeautifulSoup, tag: str, class_=None, index=0) -> str:
    if class_:
        element = element.find(tag, {"class": class_})
    else:
        element = element.find(tag)
    return element.text if element else ""


def _remove_special_chars(ch: str) -> str:
    for special in ["\\n", "\\t", "\\r"]:
        ch = ch.replace(special, "")
    return ch.strip()


def run(current_html, forecast_html):
    """Reads both pages  (current weather and forecast) and returns the dictionary. Public entry point of this unit."""
    return parse_weather_to_json(
        BeautifulSoup(current_html, "html.parser"),
        BeautifulSoup(forecast_html, "html.parser"),
    )
