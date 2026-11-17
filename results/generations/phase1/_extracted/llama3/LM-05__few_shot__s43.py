from bs4 import BeautifulSoup


def _parse_current_weather(soup: BeautifulSoup) -> dict:
    """Parse current weather data from soup to JSON."""
    weather = {"Time": "", "Temp": "", "Phrase": {}}

    current = soup.find("div", {"class": "current-weather-card"})
    weather["Time"] = current.find("p", class_="sub").text
    weather["Temp"] = remove_special_chars(
        current.find("div", {"class": "display-temp"}).text
    )
    weather["Phrase"] = remove_special_chars(
        current.find("div", {"class": "phrase"}).text
    )
    for item in current.find("div", {"class": "current-weather-details"}).find_all(
        "div", class_="detail-item"
    ):
        div = item.find_all("div")
        if len(div) < 2:
            continue
        weather["Phrase"][
            remove_special_chars(div[0].text).capitalize()
        ] = remove_special_chars(div[1].text)

    return weather


def _parse_half_day_weather(soup: BeautifulSoup) -> dict:
    """Parse half day weather data from soup to JSON."""
    weather = {"Date": "", "Temp": "", "Phrase": {}}

    card = soup.find("div", {"class": "half-day-card"})
    if "day" in card.find("h2").text.lower():
        weather_ = weather
    else:
        weather_ = weather

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


def _parse_forecast_weather(soup: BeautifulSoup) -> dict:
    """Parse forecast weather data from soup to JSON."""
    forecast = {"Date": "", "Temp": {"min": "", "max": ""}, "Precipitation": ""}

    date = soup.find("h2", {"class": "date"})
    forecast["Date"] = (
        date.find("span").text.strip() + " " + date.find_all("span")[1].text.strip()
    )
    temp = soup.find("div", {"class": "temp"})
    forecast["Temp"] = {
        "min": remove_special_chars(temp.find("span", {"class": "low"}).text.lstrip("/")),
        "max": remove_special_chars(temp.find("span", {"class": "high"}).text),
    }
    forecast["Precipitation"] = remove_special_chars(
        soup.find("div", {"class": "precip"}).text.strip()
    )

    for item in soup.find("div", {"class": "panels"}).find_all(
        "p", class_="panel-item"
    ):
        panel_ = item.text.split("\n")[0].strip()
        value_ = item.find("span").text.strip()
        forecast[
            remove_special_chars(panel_.replace(value_, ""))
        ] = remove_special_chars(value_)

    return forecast


def _parse_weather_to_json(soup: BeautifulSoup, forecast_soup: BeautifulSoup) -> dict:
    """Parse weather data from soup to JSON."""
    weather = {"current": {}, "day": {}, "night": {}, "forecast": []}

    weather["current"] = _parse_current_weather(soup)
    for card in soup.find_all("div", {"class": "half-day-card"}):
        if "day" in card.find("h2").text.lower():
            weather_ = weather["day"]
        else:
            weather_ = weather["night"]

        weather_ = _parse_half_day_weather(card)

    for wr in forecast_soup.find_all("div", {"class": "daily-wrapper"}):
        forecast = _parse_forecast_weather(wr)
        weather["forecast"].append(forecast)

    return weather


def remove_special_chars(ch: str) -> str:
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
