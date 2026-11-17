"""Command-line response with the current weather and the forecast.

Public entry point: run(data, city, country_code). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def format_current_weather(current_weather: dict) -> str:
    """Format the current weather to CLI response."""
    return colored(
        f"[*] Current Weather for {current_weather.get('city', '').capitalize()}, {current_weather.get('country_code', '').upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
        "green",
        attrs=["bold"],
    )


def format_current_details(current_weather: dict) -> str:
    """Format the current weather details to CLI response."""
    return colored(
        f" - {current_weather.get('current', {}).get('Time', 'N/A')} | Temp: {current_weather.get('current', {}).get('Temp', 'N/A')} | Feels: {current_weather.get('current', {}).get('Phrase', 'N/A')} | AQI (?)",
        "red",
    )


def format_forecast(forecast: dict) -> str:
    """Format the forecast to CLI response."""
    return colored(
        f"[*] DayTime Forecast\n"
        f" - Temp: {forecast.get('day', {}).get('Temp', 'N/A')} | Feels: {forecast.get('day', {}).get('Phrase', 'N/A')} | AQI (?)\n"
        f" - UV Index: {forecast.get('day', {}).get('Max UV Index', 'N/A')} | Wind: {forecast.get('day', {}).get('Wind', 'N/A')} | Gusts: {forecast.get('day', {}).get('Wind Gusts', 'N/A')}\n"
        f" - Cloud Cover: {forecast.get('day', {}).get('Cloud Cover', 'N/A')} | Rain: {forecast.get('day', {}).get('Rain', 'N/A')} | Thunder: {forecast.get('day', {}).get('Probability of Thunderstorms', 'N/A')}\n"
        f"[*] NightTime Forecast\n"
        f" - Temp: {forecast.get('night', {}).get('Temp', 'N/A')} | Feels: {forecast.get('night', {}).get('Phrase', 'N/A')} | AQI (?)\n"
        f" - UV Index: {forecast.get('night', {}).get('Max UV Index', 'N/A')} | Wind: {forecast.get('night', {}).get('Wind', 'N/A')} | Gusts: {forecast.get('night', {}).get('Wind Gusts', 'N/A')}\n"
        f" - Cloud Cover: {forecast.get('night', {}).get('Cloud Cover', 'N/A')} | Rain: {forecast.get('night', {}).get('Rain', 'N/A')} | Thunder: {forecast.get('night', {}).get('Probability of Thunderstorms', 'N/A')}\n"
        f"[*] Forecast for next 5 days\n"
        f" -> {', '.join([f'{item.get('Date', 'N/A')} | {item.get("Temp", {}).get("max", "N/A")} >>>>> {item.get("Temp", {}).get("min", "N/A")}' for item in forecast.get('forecast', [])[:5]])}\n"
        f"{' ' * 3}{f'- Rain: {item.get("Rain", "N/A")} | Hours of Rain: {item.get("Hours of Precipitation", "N/A")} | Cloud Cover: {item.get("Cloud Cover", "N/A")}' for item in forecast.get('forecast', [])[:5]}\n"
        f"{' ' * 3}{f'- Wind: {item.get("Wind", " N/A")[1:]} | Gusts: {item.get("Wind Gusts", "N/A")} | Thunder: {item.get("Probability of Thunderstorms", "N/A")}' for item in forecast.get('forecast', [])[:5]}\n"
        f"\n{colored('-' * 17, 'red')}{colored(f'Powered by AccuWeather ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}{colored('-' * 17, 'red')}",
        "green",
    )


def run(data, city, country_code):
    """Prints the weather in data, timing from now. Public entry point of this unit."""
    start_time = datetime.now()
    return format_forecast(data)
