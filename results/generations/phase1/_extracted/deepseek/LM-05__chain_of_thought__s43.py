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
    get_forecast_data(fcast, weather)
    return weather
