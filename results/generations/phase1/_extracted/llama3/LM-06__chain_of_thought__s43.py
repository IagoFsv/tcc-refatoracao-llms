"""Command-line response with the current weather and the forecast.

Public entry point: run(data, city, country_code). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def print_current_weather(data, city, country_code):
    """Print the current weather."""
    print(
        colored(
            f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print(
        colored(
            f" - {data.get('current', {}).get('Time', 'N/A')} | Temp: {data.get('current', {}).get('Temp', 'N/A')} | Feels: {data.get('current', {}).get('Phrase', 'N/A')} | AQI (?)",
            "red",
        )
    )
    # ... (rest of the current weather formatting)


def print_forecast(data, city, country_code):
    """Print the forecast."""
    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print(
        colored(
            f" - Temp: {data.get('day', {}).get('Temp', 'N/A')} | Feels: {data.get('day', {}).get('Phrase', 'N/A')} | AQI (?)",
            "yellow",
        )
    )
    # ... (rest of the forecast formatting)


def print_night_forecast(data, city, country_code):
    """Print the night forecast."""
    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print(
        colored(
            f" - Temp: {data.get('night', {}).get('Temp', 'N/A')} | Feels: {data.get('night', {}).get('Phrase', 'N/A')} | AQI (?)",
            "yellow",
        )
    )
    # ... (rest of the night forecast formatting)


def print_forecast_for_next_5_days(data, city, country_code):
    """Print the forecast for the next 5 days."""
    forecast = data.get("forecast", [])
    for i in range(5):
        print(
            colored(
                f" -> {forecast[i+1].get('Date', 'N/A')} | {forecast[i+1].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[i+1].get('Temp', {}).get('min', 'N/A')}",
                "magenta",
            )
        )
        # ... (rest of the forecast for the next 5 days formatting)


def fmt_cli_resp(data, city, country_code, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    print_current_weather(data, city, country_code)
    print_forecast(data, city, country_code)
    print_night_forecast(data, city, country_code)
    print_forecast_for_next_5_days(data, city, country_code)
    print(
        colored(
            "\n "
            + "-" * 17
            + f"{colored(f'Powered by AccuWeather ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}"
            + f"{colored('-'* 17, 'red')}",
            "green",
        )
    )


def run(data, city, country_code):
    """Prints the weather in data, timing from now. Public entry point of this unit."""
    return fmt_cli_resp(data, city, country_code, datetime.now())
