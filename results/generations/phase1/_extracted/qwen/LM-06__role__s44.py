"""Command-line response with the current weather and the forecast.

Public entry point: run(data, city, country_code). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def print_weather_section(data, section_key, title_color, section_title):
    """Print weather data for a specific section."""
    for key, value in data[section_key].items():
        print(
            colored(
                f" - {key.replace('_', ' ').title()}: {value if value else 'N/A'}",
                title_color,
            )
        )


def print_forecast_section(data, section_key, title_color, section_title):
    """Print forecast data for a specific section."""
    for key, value in data[section_key].items():
        print(
            colored(
                f" - {key.replace('_', ' ').title()}: {value if value else 'N/A'}",
                title_color,
            )
        )


def fmt_cli_resp(data, city: str, country_code, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    print(
        colored(
            f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print_weather_section(data, "current", "red", "Current Weather")

    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print_weather_section(data, "day", "yellow", "DayTime Forecast")

    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print_weather_section(data, "night", "green", "NightTime Forecast")

    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print(
            colored(
                f" -> {forecast[i+1].get('Date', 'N/A')} | {forecast[i+1].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[i+1].get('Temp', {}).get('min', 'N/A')}",
                "magenta",
            )
        )
        print_forecast_section(forecast[i+1], "Temp", "green", "Temperature")
        print_forecast_section(forecast[i+1], "Wind", "yellow", "Wind")

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
