from bs4 import BeautifulSoup


def parse_current_weather(soup: BeautifulSoup) -> dict:
    """Parse current weather data from soup."""
    current = soup.find("div", {"class": "current-weather-card"})
    weather = {
        "Time": current.find("p", class_="sub").text,
        "Temp": remove_special_chars(current.find("div", {"class": "display-temp"}).text),
        "Phrase": remove_special_chars(current.find("div", {"class": "phrase"}).text),
    }
    details = current.find("div", {"class": "current-weather-details"}).find_all(
        "div", class_="detail-item"
    )
    for item in details:
        div = item.find_all("div")
        if len(div) < 2:
            continue
        key = remove_special_chars(div[0].text).capitalize()
        value = remove_special_chars(div[1].text)
        weather[key] = value
    return weather


def parse_day_and_night_weather(soup: BeautifulSoup) -> dict:
    """Parse day and night weather data from soup."""
    weather = {}
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
        panels = card.find("div", {"class": "panels"}).find_all("p", class_="panel-item")
        for item in panels:
            panel_ = item.text.split("\n")[0].strip()
            value_ = item.find("span").text.strip()
            weather_[remove_special_chars(panel_.replace(value_, ""))] = value_
    return weather


def parse_forecast(soup: BeautifulSoup) -> dict:
    """Parse forecast data from soup."""
    forecast = []
    for wr in soup.find_all("div", {"class": "daily-wrapper"}):
        forecast_item = {}
        date = wr.find("h2", {"class": "date"})
        forecast_item["Date"] = (
            date.find("span").text.strip() + " " + date.find_all("span")[1].text.strip()
        )
        temp = wr.find("div", {"class": "temp"})
        forecast_item["Temp"] = {
            "min": remove_special_chars(temp.find("span", {"class": "low"}).text.lstrip("/")),
            "max": remove_special_chars(temp.find("span", {"class": "high"}).text),
        }
        forecast_item["Precipitation"] = remove_special_chars(
            wr.find("div", {"class": "precip"}).text.strip()
        )
        panels = wr.find("div", {"class": "panels"}).find_all("p", class_="panel-item")
        for item in panels:
            panel_ = item.text.split("\n")[0].strip()
            value_ = item.find("span").text.strip()
            forecast_item[
                remove_special_chars(panel_.replace(value_, ""))
            ] = value_
        forecast.append(forecast_item)
    return forecast


def parse_weather_to_json(soup: BeautifulSoup, fcast: BeautifulSoup) -> dict:
    """Parse weather data from soup to JSON."""
    weather = {
        "current": {},
        "day": {},
        "night": {},
        "forecast": [],
    }
    weather["current"] = parse_current_weather(soup)
    weather["day"], weather["night"] = parse_day_and_night_weather(soup).values()
    weather["forecast"] = parse_forecast(fcast)
    return weather


def remove_special_chars(ch: str) -> str:
    """Remove special chars from string."""
    for special in ["\\n", "\\t", "\\r"]:
        ch = ch.replace(special, "")

    return ch.strip()


def executar(html_atual, html_previsao):
    """Le as duas paginas (clima atual e previsao) e devolve o dicionario. Ponto de entrada publico desta unidade."""
    return parse_weather_to_json(
        BeautifulSoup(html_atual, "html.parser"),
        BeautifulSoup(html_previsao, "html.parser"),
    )
