from bs4 import BeautifulSoup

def parse_weather_to_json(soup: BeautifulSoup, fcast: BeautifulSoup) -> dict:
    """Parse weather data from soup to JSON."""
    weather = {
        "current": {},
        "day": {},
        "night": {},
        "forecast": [],
    }

    parse_current_weather(soup, weather)
    parse_day_and_night_weather(soup, weather)
    parse_forecast_data(fcast, weather)

    return weather

def parse_current_weather(soup: BeautifulSoup, weather: dict):
    """Parse current weather data from soup to weather dictionary."""
    current = soup.find("div",  {"class": "current-weather-card"})
    weather["current"]["Time"] = current.find("p", class_="sub").text
    weather["current"]["Temp"] = remove_special_chars(current.find("div", {"class": "display-temp"}).text)
    weather["current"]["Phrase"] = remove_special_chars(current.find("div", {"class": "phrase"}).text)
    parse_current_weather_details(current, weather)

def parse_current_weather_details(current: BeautifulSoup, weather: dict):
    """Parse current weather details from soup to weather dictionary."""
    for item in current.find("div", {"class": "current-weather-details"}).find_all("div", class_="detail-item"):
        div = item.find_all("div")
        if len(div) < 2:
            continue
        weather["current"][remove_special_chars(div[0].text).capitalize()] = remove_special_chars(div[1].text)

def parse_day_and_night_weather(soup: BeautifulSoup, weather: dict):
    """Parse day and night weather data from soup to weather dictionary."""
    for card in soup.find_all("div", {"class": "half-day-card"}):
        weather_ = weather["day"] if "day" in card.find("h2").text.lower() else weather["night"]
        parse_day_and_night_weather_data(card, weather_)

def parse_day_and_night_weather_data(card: BeautifulSoup, weather: dict):
    """Parse day and night weather data from soup to weather dictionary."""
    weather["Date"] = card.find("span", class_="short-date").text.strip()
    weather["Temp"] = remove_special_chars(card.find("div", {"class": "temperature"}).text.strip().split("°")[0] + "°")
    weather["Phrase"] = remove_special_chars(card.find("div", {"class": "phrase"}).text.strip())
    parse_day_and_night_weather_details(card, weather)

def parse_day_and_night_weather_details(card: BeautifulSoup, weather: dict):
    """Parse day and night weather details from soup to weather dictionary."""
    for item in card.find("div", {"class": "panels"}).find_all("p", class_="panel-item"):
        panel_ = item.text.split("\n")[0].strip()
        value_ = item.find("span").text.strip()
        weather[remove_special_chars(panel_.replace(value_, ""))] = remove_special_chars(value_)

def parse_forecast_data(fcast: BeautifulSoup, weather: dict):
    """Parse forecast data from soup to weather dictionary."""
    for wr in fcast.find_all("div", {"class": "daily-wrapper"}):
        forecast = {}
        parse_forecast_data_date_and_temp(wr, forecast)
        parse_forecast_data_details(wr, forecast)
        weather["forecast"].append(forecast)

def parse_forecast_data_date_and_temp(wr: BeautifulSoup, forecast: dict):
    """Parse forecast data from soup to forecast dictionary."""
    date = wr.find("h2", {"class": "date"})
    forecast["Date"] = date.find("span").text.strip() + " " + date.find_all("span")[1].text.strip()
    temp = wr.find("div", {"class": "temp"})
    forecast["Temp"] = {"min": remove_special_chars(temp.find("span", {"class": "low"}).text.lstrip("/")), "max": remove_special_chars(temp.find("span", {"class": "high"}).text)}
    forecast["Precipitation"] = remove_special_chars(wr.find("div", {"class": "precip"}).text.strip())

def parse_forecast_data_details(wr: BeautifulSoup, forecast: dict):
    """Parse forecast data details from soup to forecast dictionary."""
    for item in wr.find("div", {"class": "panels"}).find_all("p", class_="panel-item"):
        panel_ = item.text.split("\n")[0].strip()
        value_ = item.find("span").text.strip()
        forecast[remove_special_chars(panel_.replace(value_, ""))] = remove_special_chars(value_)

def remove_special_chars(ch: str) -> str:
    """Remove special chars from string."""
    for special in ["\\n", "\\t", "\\r"]:
        ch = ch.replace(special, "")
    return ch.strip()

def executar(html_atual, html_previsao):
    """Le as duas paginas (clima atual e previsao) e devolve o dicionario. Ponto de entrada publico desta unidade."""
    return parse_weather_to_json(BeautifulSoup(html_atual, "html.parser"), BeautifulSoup(html_previsao, "html.parser"))
