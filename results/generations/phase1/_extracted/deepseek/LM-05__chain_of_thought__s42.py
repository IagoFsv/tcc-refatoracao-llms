from bs4 import BeautifulSoup

def parse_weather_to_json(soup: BeautifulSoup, fcast: BeautifulSoup) -> dict:
    """Parse weather data from soup to JSON."""
    weather = {"current": {}, "day": {}, "night": {}, "forecast": []}

    # Get current weather data
    current = soup.find("div", {"class": "current-weather-card"})
    extract_current_weather_data(current, weather)

    # Get day and night weather data
    for card in soup.find_all("div", {"class": "half-day-card"}):
        weather_ = weather["day"] if "day" in card.find("h2").text.lower() else weather["night"]
        extract_day_night_weather_data(card, weather_)

    # get forecast data
    for wr in fcast.find_all("div", {"class": "daily-wrapper"}):
        forecast = {}
        extract_forecast_data(wr, forecast)
        weather["forecast"].append(forecast)

    return weather

def extract_current_weather_data(current, weather):
    """Extract current weather data."""
    weather["current"]["Time"] = current.find("p", class_="sub").text
    weather["current"]["Temp"] = remove_special_chars(current.find("div", {"class": "display-temp"}).text)
    weather["current"]["Phrase"] = remove_special_chars(current.find("div", {"class": "phrase"}).text)
    for item in current.find("div", {"class": "current-weather-details"}).find_all("div", class_="detail-item"):
        div = item.find_all("div")
        if len(div) < 2:
            continue
        weather["current"][remove_special_chars(div[0].text).capitalize()] = remove_special_chars(div[1].text)

def extract_day_night_weather_data(card, weather_):
    """Extract day and night weather data."""
    weather_["Date"] = card.find("span", class_="short-date").text.strip()
    weather_["Temp"] = remove_special_chars(card.find("div", {"class": "temperature"}).text.strip().split("°")[0] + "°")
    weather_["Phrase"] = remove_special_chars(card.find("div", {"class": "phrase"}).text.strip())
    for item in card.find("div", {"class": "panels"}).find_all("p", class_="panel-item"):
        panel_ = item.text.split("\n")[0].strip()
        value_ = item.find("span").text.strip()
        weather_[remove_special_chars(panel_.replace(value_, ""))] = remove_special_chars(value_)

def extract_forecast_data(wr, forecast):
    """Extract forecast data."""
    forecast["Date"] = (wr.find("h2", {"class": "date"}).find("span").text.strip() + " " + wr.find("h2", {"class": "date"}).find_all("span")[1].text.strip())
    forecast["Temp"] = {"min": remove_special_chars(wr.find("div", {"class": "temp"}).find("span", {"class": "low"}).text.lstrip("/")), "max": remove_special_chars(wr.find("div", {"class": "temp"}).find("span", {"class": "high"}).text)}
    forecast["Precipitation"] = remove_special_chars(wr.find("div", {"class": "precip"}).text.strip())
    for item in card.find("div", {"class": "panels"}).find_all("p", class_="panel-item"):
        panel_ = item.text.split("\n")[0].strip()
        value_ = item.find("span").text.strip()
        forecast[remove_special_chars(panel_.replace(value_, ""))] = remove_special_chars(value_)

def remove_special_chars(ch: str) -> str:
    """Remove special chars from string."""
    for special in ["\\n", "\\t", "\\r"]:
        ch = ch.replace(special, "")
    return ch.strip()

def run(current_html, forecast_html):
    """Reads both pages (current weather and forecast) and returns the dictionary. Public entry point of this unit."""
    return parse_weather_to_json(BeautifulSoup(current_html, "html.parser"), BeautifulSoup(forecast_html, "html.parser"))
