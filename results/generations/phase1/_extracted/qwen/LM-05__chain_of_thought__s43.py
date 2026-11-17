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

    # Get current weather data
    weather["current"] = extract_current_weather(soup)

    # Get day and night weather data
    for card in soup.find_all("div", {"class": "half-day-card"}):
        weather_ = extract_day_night_weather(card)
        if "day" in card.find("h2").text.lower():
            weather["day"] = weather_
        else:
            weather["night"] = weather_

    # get forecast data
    for wr in fcast.find_all("div", {"class": "daily-wrapper"}):
        weather["forecast"].append(extract_forecast(wr))

    return weather


def extract_current_weather(soup: BeautifulSoup) -> dict:
    """Extract current weather data from the HTML."""
    current = soup.find("div", {"class": "current-weather-card"})
    weather = {
        "Time": current.find("p", class_="sub").text,
        "Temp": remove_special_chars(
            current.find("div", {"class": "display-temp"}).text
        ),
        "Phrase": remove_special_chars(
            current.find("div", {"class": "phrase"}).text
        ),
    }
    for item in current.find("div", {"class": "current-weather-details"}).find_all(
        "div", class_="detail-item"
    ):
        div = item.find_all("div")
        if len(div) < 2:
            continue
        weather[
            remove_special_chars(div[0].text).capitalize()
        ] = remove_special_chars(div[1].text)
    return weather


def extract_day_night_weather(card: BeautifulSoup) -> dict:
    """Extract day or night weather data from the HTML."""
    weather = {
        "Date": card.find("span", class_="short-date").text.strip(),
        "Temp": remove_special_chars(
            card.find("div", {"class": "temperature"}).text.strip().split("°")[0] + "°"
        ),
        "Phrase": remove_special_chars(
            card.find("div", {"class": "phrase"}).text.strip()
        ),
    }
    for item in card.find("div", {"class": "panels"}).find_all(
        "p", class_="panel-item"
    ):
        panel_ = item.text.split("\n")[0].strip()
        value_ = item.find("span").text.strip()
        weather[
            remove_special_chars(panel_.replace(value_, ""))
        ] = remove_special_chars(value_)
    return weather


def extract_forecast(wr: BeautifulSoup) -> dict:
    """Extract forecast data from the HTML."""
    forecast = {
        "Date": wr.find("h2", {"class": "date"}).find("span").text.strip() + " " + wr.find("h2", {"class": "date"}).find_all("span")[1].text.strip(),
        "Temp": {
            "min": remove_special_chars(wr.find("div", {"class": "temp"}).find("span", {"class": "low"}).text.lstrip("/")),
            "max": remove_special_chars(wr.find("div", {"class": "temp"}).find("span", {"class": "high"}).text),
        },
        "Precipitation": remove_special_chars(
            wr.find("div", {"class": "precip"}).text.strip()
        ),
    }
    for item in wr.find("div", {"class": "panels"}).find_all(
        "p", class_="panel-item"
    ):
        panel_ = item.text.split("\n")[0].strip()
        value_ = item.find("span").text.strip()
        forecast[
            remove_special_chars(panel_.replace(value_, ""))
        ] = remove_special_chars(value_)
    return forecast


def remove_special_chars(ch: str) -> str:
    """Remove special chars from string."""
    for special in ["\\n", "\\t", "\\r"]:
        ch = ch.replace(special, "")

    return ch.strip()


def run(current_html, forecast_html):
    """Reads both pages (current weather and forecast) and returns the dictionary. Public entry point of this unit."""
    return parse_weather_to_json(
        BeautifulSoup(current_html, "html.parser"),
        BeautifulSoup(forecast_html, "html.parser"),
    )
