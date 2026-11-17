"""Extraction of weather data from HTML pages into a dictionary.

Public entry point: run(current_html, forecast_html). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

from bs4 import BeautifulSoup


def _parse_current_weather(soup):
    current = soup.find("div", {"class": "current-weather-card"})
    return {
        "Time": current.find("p", class_="sub").text,
        "Temp": remove_special_chars(
            current.find("div", {"class": "display-temp"}).text
        ),
        "Phrase": remove_special_chars(
            current.find("div", {"class": "phrase"}).text
        ),
        **{
            remove_special_chars(div[0].text).capitalize(): remove_special_chars(div[1].text)
            for item in current.find("div", {"class": "current-weather-details"}).find_all(
                "div", class_="detail-item"
            )
            if len(div) == 2
        },
    }


def _parse_half_day_weather(soup, weather_key):
    weather = {}
    for card in soup.find_all("div", {"class": "half-day-card"}):
        if weather_key in card.find("h2").text.lower():
            weather_ = weather[weather_key]
        else:
            weather_ = weather[weather_key]

        weather_["Date"] = card.find("span", class_="short-date").text.strip()
        weather_["Temp"] = remove_special_chars(
            card.find("div", {"class": "temperature"}).text.strip().split("°")[0] + "°"
        )
        weather_["Phrase"] = remove_special_chars(
            card.find("div", {"class": "phrase"}).text.strip()
        )

        for item in card.find("div", {"class": "panels"}).find_all(
            "p", class_="panel-item"
        ):
            panel_ = item.text.split("\n")[0].strip()
            value_ = item.find("span").text.strip()
            weather_[
                remove_special_chars(panel_.replace(value_, ""))
            ] = remove_special_chars(value_)

    return weather


def _parse_forecast(soup):
    forecast = []
    for wr in soup.find_all("div", {"class": "daily-wrapper"}):
        forecast_data = {}

        date = wr.find("h2", {"class": "date"})
        forecast_data["Date"] = (
            date.find("span").text.strip() + " " + date.find_all("span")[1].text.strip()
        )
        temp = wr.find("div", {"class": "temp"})
        forecast_data["Temp"] = {
            "min": remove_special_chars(temp.find("span", {"class": "low"}).text.lstrip("/")),
            "max": remove_special_chars(temp.find("span", {"class": "high"}).text),
        }
        forecast_data["Precipitation"] = remove_special_chars(
            wr.find("div", {"class": "precip"}).text.strip()
        )
        for item in wr.find("div", {"class": "panels"}).find_all(
            "p", class_="panel-item"
        ):
            panel_ = item.text.split("\n")[0].strip()
            value_ = item.find("span").text.strip()
            forecast_data[
                remove_special_chars(panel_.replace(value_, ""))
            ] = remove_special_chars(value_)
        forecast.append(forecast_data)

    return forecast


def _parse_weather_to_json(soup, fcast):
    weather = {
        "current": _parse_current_weather(soup),
        "day": _parse_half_day_weather(soup, "day"),
        "night": _parse_half_day_weather(soup, "night"),
        "forecast": _parse_forecast(fcast),
    }

    return weather


def remove_special_chars(ch):
    """Remove special chars from string."""
    for special in ["\\n", "\\t", "\\r"]:
        ch = ch.replace(special, "")

    return ch.strip()


def run(current_html, forecast_html):
    """Reads both pages (current weather and forecast) and returns the dictionary. Public entry point of this unit."""
    return _parse_weather_to_json(
        BeautifulSoup(current_html, "html.parser"),
        BeautifulSoup(forecast_html, "html.parser"),
    )
