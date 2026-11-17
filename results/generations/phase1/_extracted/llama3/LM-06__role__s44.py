"""Command-line response with the current weather and the forecast.

Public entry point: run(data, city, country_code). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def format_current_weather(data, city: str, country_code: str) -> str:
    """Format the current weather data to CLI response."""
    return colored(
        f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
        "green",
        attrs=["bold"],
    )


def format_current_details(data, city: str, country_code: str) -> str:
    """Format the current weather details to CLI response."""
    return colored(
        f" - {data.get('current', {}).get('Time', 'N/A')} | Temp: {data.get('current', {}).get('Temp', 'N/A')} | Feels: {data.get('current', {}).get('Phrase', 'N/A')} | AQI (?)",
        "red",
    )


def format_forecast(data, city: str, country_code: str) -> str:
    """Format the forecast to CLI response."""
    return colored(
        f"[*] DayTime Forecast",
        "red",
        attrs=["bold"],
    )


def format_day_forecast(data, city: str, country_code: str) -> str:
    """Format the day forecast to CLI response."""
    return colored(
        f" - Temp: {data.get('day', {}).get('Temp', 'N/A')} | Feels: {data.get('day', {}).get('Phrase', 'N/A')} | AQI (?)",
        "yellow",
    )


def format_night_forecast(data, city: str, country_code: str) -> str:
    """Format the night forecast to CLI response."""
    return colored(
        f" - Temp: {data.get('night', {}).get('Temp', 'N/A')} | Feels: {data.get('night', {}).get('Phrase', 'N/A')} | AQI (?)",
        "yellow",
    )


def format_forecast_next_days(data, city: str, country_code: str) -> str:
    """Format the forecast for next 5 days to CLI response."""
    forecast = data.get("forecast", [])
    forecast_str = ""
    for i in range(5):
        forecast_str += colored(
            f" -> {forecast[i+1].get('Date', 'N/A')} | {forecast[i+1].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[i+1].get('Temp', {}).get('min', 'N/A')}",
            "magenta",
        )
        forecast_str += colored(
            " " * 3
            + f"- Rain: {forecast[i+1].get('Rain', 'N/A')} | Hours of Rain: {forecast[i+1].get('Hours of Precipitation', 'N/A')} | Cloud Cover: {forecast[i+1].get('Cloud Cover', 'N/A')}",
            "green",
        )
        forecast_str += colored(
            " " * 3
            + f"- Wind: {forecast[i+1].get('Wind', ' N/A')[1:]} | Gusts: {forecast[i+1].get('Wind Gusts', 'N/A')} | Thunder: {forecast[i+1].get('Probability of Thunderstorms', 'N/A')}",
            "yellow",
        )
        forecast_str += "\n"
    return forecast_str


def run(data, city, country_code):
    """Prints the weather in data, timing from now. Public entry point of this unit."""
    return fmt_cli_resp(data, city, country_code, datetime.now())
