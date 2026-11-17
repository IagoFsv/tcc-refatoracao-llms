"""Extraction of weather data from HTML pages into a dictionary.

Public entry point: run(current_html, forecast_html). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

from bs4 import BeautifulSoup


def parse_weather_to_json(soup: BeautifulSoup, fcast: BeautifulSoup) -> dict:
    """Parse weather data from soup to JSON."""
    weather = {
        "current": {},
        "day": {},
        "night": {},
        "forecast": [],
    }

    _parse_current_weather(soup, weather)
    _parse_day_and_night_weather(soup, weather)
    _parse_forecast_data(fcast, weather)

    return weather


def _parse_current_weather(soup, weather):
    current = soup.find("div",  {"class": "current-weather-card"})
    weather["current"]["Time"] = current.find("p", class_="sub").text
    weather["current"]["Temp"] = remove_special_chars(
        current.find("div",  {"class": "display-temp"}).text
    )
    weather["current"]["Phrase"] = remove_special_chars(
        current.find("div",  {"class": "phrase"}).text
    )
    _parse_current_details(current, weather["current"])


def _parse_current_details(current, weather_current):
    for item in current.find("div",  {"class": "current-weather-details"}).find_all(
        "div", class_="detail-item"
    ):
        div = item.find_all("div")
        if len(div) < 2:
            continue
        weather_current[
            remove_special_chars(div[0].text).capitalize()
        ] = remove_special_chars(div[1].text)


def _parse_day_and_night_weather(soup, weather):
    for card in soup.find_all("div",  {"class": "half-day-card"}):
        if "day" in card.find("h2").text.lower():
            weather_ = weather["day"]
        else:
            weather_ = weather["night"]

        weather_["Date"] = card.find("span", class_="short-date").text.strip()
        weather_["Temp"] = remove_special_chars(
            card.find("div",  {"class": "temperature"}).text.strip().split("°")[0] + "°"
        )
        weather_["Phrase"] = remove_special_chars(
            card.find("div",  {"class": "phrase"}).text.strip()
        )
        _parse_weather_details(card, weather_)


def _parse_weather_details(card, weather_):
    for item in card.find("div",  {"class": "panels"}).find_all(
        "p", class_="panel-item"
    ):
        panel_ = item.text.split("\n")[0].strip()
        value_ = item.find("span").text.strip()
        weather_[
            remove_special_chars(panel_.replace(value_, ""))
        ] = remove_special_chars(value_)


def _parse_forecast_data(fcast, weather):
    for wr in fcast.find_all("div",  {"class": "daily-wrapper"}):
        forecast = {}

        date = wr.find("h2",  {"class": "date"})
        forecast["Date"] = (
            date.find("span").text.strip() + " " + date.find_all("span")[1].text.strip()
        )
        temp = wr.find("div",  {"class": "temp"})
        forecast["Temp"] = {
            "min": remove_special_chars(temp.find("span",  {"class": "low"}).text.lstrip("/")),
            "max": remove_special_chars(temp.find("span",  {"class": "high"}).text),
        }
        forecast["Precipitation"] = remove_special_chars(
            wr.find("div",  {"class": "precip"}).text.strip()
        )
        _parse_forecast_details(wr, forecast)
        weather["forecast"].append(forecast)


def _parse_forecast_details(wr, forecast):
    for item in wr.find("div",  {"class": "panels"}).find_all(
        "p", class_="panel-item"
    ):
        panel_ = item.text.split("\n")[0].strip()
        value_ = item.find("span").text.strip()
        forecast[
            remove_special_chars(panel_.replace(value_, ""))
        ] = remove_special_chars(value_)


def remove_special_chars(ch: str) -> str:
    """Remove special chars from string."""
    for special in ["\\n", "\\t", "\\r"]:
        ch = ch.replace(special, "")

    return ch.strip()


def run(current_html, forecast_html):
    """Reads both pages  (current weather and forecast) and returns the dictionary. Public entry point of this unit."""
    return parse_weather_to_json(
        BeautifulSoup(current_html, "html.parser"),
        BeautifulSoup(forecast_html, "html.parser"),
    )
