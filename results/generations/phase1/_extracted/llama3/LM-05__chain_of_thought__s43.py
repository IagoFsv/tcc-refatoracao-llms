def parse_current_weather(soup: BeautifulSoup) -> dict:
    """Parse current weather data from soup to JSON."""
    current = soup.find("div", {"class": "current-weather-card"})
    weather = {
        "Time": current.find("p", class_="sub").text,
        "Temp": remove_special_chars(current.find("div", {"class": "display-temp"}).text),
        "Phrase": remove_special_chars(current.find("div", {"class": "phrase"}).text),
    }
    for item in current.find("div", {"class": "current-weather-details"}).find_all("div", class_="detail-item"):
        div = item.find_all("div")
        if len(div) < 2:
            continue
        weather[
            remove_special_chars(div[0].text).capitalize()
        ] = remove_special_chars(div[1].text)
    return weather

def parse_day_and_night_weather(soup: BeautifulSoup) -> dict:
    """Parse day and night weather data from soup to JSON."""
    weather = {"day": {}, "night": {}}
    for card in soup.find_all("div", {"class": "half-day-card"}):
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
            weather_[
                remove_special_chars(panel_.replace(value_, ""))
            ] = remove_special_chars(value_)
    return weather

def parse_forecast_weather(soup: BeautifulSoup) -> dict:
    """Parse forecast weather data from soup to JSON."""
    forecast = []
    for wr in soup.find_all("div", {"class": "daily-wrapper"}):
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
            forecast_[
                remove_special_chars(panel_.replace(value_, ""))
            ] = remove_special_chars(value_)
        forecast.append(forecast_)
    return forecast

def parse_weather_to_json(soup: BeautifulSoup, fcast: BeautifulSoup) -> dict:
    """Parse weather data from soup to JSON."""
    weather = {
        "current": parse_current_weather(soup),
        "day": {},
        "night": {},
        "forecast": parse_forecast_weather(fcast),
    }
    return weather

def run(current_html, forecast_html):
    """Reads both pages (current weather and forecast) and returns the dictionary. Public entry point of this unit."""
    return parse_weather_to_json(
        BeautifulSoup(current_html, "html.parser"),
        BeautifulSoup(forecast_html, "html.parser"),
    )
