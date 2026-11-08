from bs4 import BeautifulSoup


def extract_current_weather(soup: BeautifulSoup) -> dict:
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


def extract_day_night_weather(soup: BeautifulSoup) -> dict:
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

        for item in card.find("div", {"class": "panels"}).find_all(
            "p", class_="panel-item"
        ):
            panel_ = item.text.split("\n")[0].strip()
            value_ = item.find("span").text.strip()
            weather_[
                remove_special_chars(panel_.replace(value_, ""))
            ] = remove_special_chars(value_)
    return weather


def extract_forecast(fcast: BeautifulSoup) -> list:
    forecast_list = []
    for wr in fcast.find_all("div", {"class": "daily-wrapper"}):
        forecast = {}

        date = wr.find("h2", {"class": "date"})
        forecast["Date"] = (
            date.find("span").text.strip() + " " + date.find_all("span")[1].text.strip()
        )
        temp = wr.find("div", {"class": "temp"})
        forecast["Temp"] = {
            "min": remove_special_chars(temp.find("span", {"class": "low"}).text.lstrip("/")),
            "max": remove_special_chars(temp.find("span", {"class": "high"}).text),
        }
        forecast["Precipitation"] = remove_special_chars(
            wr.find("div", {"class": "precip"}).text.strip()
        )
        for item in wr.find("div", {"class": "panels"}).find_all(
            "p", class_="panel-item"
        ):
            panel_ = item.text.split("\n")[0].strip()
            value_ = item.find("span").text.strip()
            forecast[
                remove_special_chars(panel_.replace(value_, ""))
            ] = remove_special_chars(value_)
        forecast_list.append(forecast)
    return forecast_list


def parse_weather_to_json(soup: BeautifulSoup, fcast: BeautifulSoup) -> dict:
    weather = {
        "current": extract_current_weather(soup),
        "day": extract_day_night_weather(soup)["day"],
        "night": extract_day_night_weather(soup)["night"],
        "forecast": extract_forecast(fcast),
    }
    return weather


def remove_special_chars(ch: str) -> str:
    for special in ["\\n", "\\t", "\\r"]:
        ch = ch.replace(special, "")

    return ch.strip()


def executar(html_atual, html_previsao):
    return parse_weather_to_json(
        BeautifulSoup(html_atual, "html.parser"),
        BeautifulSoup(html_previsao, "html.parser"),
    )
