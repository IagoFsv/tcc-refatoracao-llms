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
    _parse_day_night_weather(soup, weather)
    _parse_forecast(fcast, weather)

    return weather

def _parse_current_weather(soup: BeautifulSoup, weather: dict):
    current = soup.find("div", {"class": "current-weather-card"})
    _parse_weather_data(current, weather["current"])

def _parse_day_night_weather(soup: BeautifulSoup, weather: dict):
    for card in soup.find_all("div", {"class": "half-day-card"}):
        weather_ = weather["day"] if "day" in card.find("h2").text.lower() else weather["night"]
        _parse_weather_data(card, weather_)

def _parse_forecast(fcast: BeautifulSoup, weather: dict):
    for wr in fcast.find_all("div", {"class": "daily-wrapper"}):
        forecast = _parse_forecast_data(wr)
        weather["forecast"].append(forecast)

def _parse_weather_data(item, weather_data):
    weather_data["Time"] = item.find("p", class_="sub").text
    weather_data["Temp"] = remove_special_chars(item.find("div", {"class": "display-temp"}).text)
    weather_data["Phrase"] = remove_special_chars(item.find("div", {"class": "phrase"}).text)

    for weather_item in item.find("div", {"class": "current-weather-details"}).find_all("div", class_="detail-item"):
        div = weather_item.find_all("div")
        if len(div) < 2:
            continue
        weather_data[remove_special_chars(div[0].text).capitalize()] = remove_special_chars(div[1].text)

def _parse_forecast_data(item):
    forecast = {}
    date = item.find("h2", {"class": "date"})
    forecast["Date"] = f"{date.find('span').text.strip()} {date.find_all('span')[1].text.strip()}"
    temp = item.find("div", {"class": "temp"})
    forecast["Temp"] = {"min": remove_special_chars(temp.find("span", {"class": "low"}).text.lstrip("/")),
                        "max": remove_special_chars(temp.find("span", {"class": "high"}).text)}
    forecast["Precipitation"] = remove_special_chars(item.find("div", {"class": "precip"}).text.strip())
    return forecast

def remove_special_chars(ch: str) -> str:
    """Remove special chars from string."""
    for special in ["\\n", "\\t", "\\r"]:
        ch = ch.replace(special, "")

    return ch.strip()

def executar(html_atual, html_previsao):
    """Le as duas paginas  (clima atual e previsao) e devolve o dicionario. Ponto de entrada publico desta unidade."""
    return parse_weather_to_json(
        BeautifulSoup(html_atual, "html.parser"),
        BeautifulSoup(html_previsao, "html.parser"),
    )
