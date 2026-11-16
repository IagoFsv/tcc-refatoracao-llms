def parse_weather_to_json(soup: BeautifulSoup, fcast: BeautifulSoup) -> dict:
    weather = {
        "current": {},
        "day": {},
        "night": {},
        "forecast": [],
    }

    current_weather = get_current_weather(soup)
    weather["current"] = current_weather

    day_and_night_weather = get_day_and_night_weather(soup)
    weather["day"] = day_and_night_weather["day"]
    weather["night"] = day_and_night_weather["night"]

    forecast = get_forecast(fcast)
    weather["forecast"] = forecast

    return weather

def get_current_weather(soup: BeautifulSoup) -> dict:
    # ...

def get_day_and_night_weather(soup: BeautifulSoup) -> dict:
    # ...

def get_forecast(fcast: BeautifulSoup) -> list:
    # ...

def remove_special_chars(ch: str) -> str:
    # ...

def executar(html_atual, html_previsao):
    return parse_weather_to_json(
        BeautifulSoup(html_atual, "html.parser"),
        BeautifulSoup(html_previsao, "html.parser"),
    )
