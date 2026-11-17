"""Command-line response with the current weather and the forecast.

Public entry point: run(data, city, country_code). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a,  %d-%b-%y")


def print_current_weather(data, city: str, country_code: str, start_time: datetime):
    """Print the current weather data."""
    print(
        colored(
            f"[*] Current Weather for  {city.capitalize()},  {country_code.upper()}  [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print(
        colored(
            f"  -  {data.get('current', {}).get('Time', 'N/A')} | Temp:  {data.get('current', {}).get('Temp', 'N/A')} | Feels:  {data.get('current', {}).get('Phrase', 'N/A')} | AQI  (?)",
            "red",
        )
    )
    print(
        colored(
            f"  - RealFeel Sun:  {data.get('current', {}).get('Realfeel sun', 'N/A')} | RealFeel Shade:  {data.get('current', {}).get('Realfeel shade', 'N/A')} | UV Index:  {data.get('current', {}).get('Max uv index', 'N/A')}",
            "blue",
        )
    )
    print(
        colored(
            f"  - Wind:  {data.get('current', {}).get('Wind', ' N/A')[1:]} | Gusts:  {data.get('current', {}).get('Wind gusts', 'N/A')} | Cloud Cover:  {data.get('current', {}).get('Cloud cover', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f"  - Dew Point:  {data.get('current', {}).get('Dew point', 'N/A')} | Humidity:  {data.get('current', {}).get('Humidity', 'N/A')} | Indoor Humidity:  {data.get('current', {}).get('Indoor humidity', 'N/A')}",
            "cyan",
        )
    )
    print(
        colored(
            f"  - Visibility:  {data.get('current', {}).get('Visibility', 'N/A')} | Pressure:  {data.get('current', {}).get('Pressure', 'N/A')} | Ceiling:  {data.get('current', {}).get('Cloud ceiling', 'N/A')}",
            "yellow",
        )
    )


def print_forecast(data, start_time: datetime):
    """Print the weather forecast data."""
    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print_weather_data(data.get('day', {}))

    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print_weather_data(data.get('night', {}))

    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print_forecast_data(forecast[i+1])
    print(
        colored(
             "\n  "
            + "-" * 17
            + f"{colored(f'Powered by AccuWeather  ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}"
            + f"{colored('-' * 17, 'red')}",
            "green",
        )
    )


def print_weather_data(data):
    """Print weather data."""
    print(
        colored(
            f"  - Temp:  {data.get('Temp', 'N/A')} | Feels:  {data.get('Phrase', 'N/A')} | AQI  (?)",
            "yellow",
        )
    )
    print(
        colored(
            f"  - UV Index:  {data.get('Max UV Index', 'N/A')} | Wind:  {data.get('Wind', 'N/A')[1:]} | Gusts:  {data.get('Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f"  - Cloud Cover:  {data.get('Cloud Cover', 'N/A')} | Rain:  {data.get('Rain', 'N/A')} | Thunder:  {data.get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )


def print_forecast_data(data):
    """Print forecast data."""
    print(
        colored(
            f"  -> {data.get('Date', 'N/A')} | {data.get('Temp', {}).get('max', 'N/A')} >>>>> {data.get('Temp', {}).get('min', 'N/A')}",
            "magenta",
        )
    )
    print_weather_data(data)


def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    print_current_weather(data, city, country_code, start_time)
    print_forecast(data, start_time)


def run(data, city, country_code):
    """Prints the weather in data, timing from now. Public entry point of this unit."""
    return fmt_cli_resp(data, city, country_code, datetime.now())
