from bs4 import BeautifulSoup

def parse_weather_to_json(soup: BeautifulSoup, fcast: BeautifulSoup) -> dict:
    """Parse weather data from soup to JSON."""
    weather = {
        "current": {},
        "day": {},
        "night": {},
        "forecast": [],
    }

    get_current_weather(soup, weather)
    get_day_night_weather(soup, weather)
    get_forecast_weather(soup, fcast, weather)

    return weather

def get_current_weather(soup, weather):
    current = soup.find("div", {"class": "current-weather-card"})
    # ... código para obter os dados de clima atual ...

def get_day_night_weather(soup, weather):
    # ... código para obter os dados de clima do dia e da noite ...

def get_forecast_weather(soup, fcast, weather):
    # ... código para obter os dados de previsão ...

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
