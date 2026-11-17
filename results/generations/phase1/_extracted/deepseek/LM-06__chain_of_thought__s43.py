"""Command-line response with the current weather and the forecast.

Public entry point: run(data, city, country_code). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a,  %d-%b-%y")


def print_current_weather(data, city, country_code):
    """Print current weather details."""
    print(
        colored(
            f"[*] Current Weather for  {city.capitalize()},  {country_code.upper()}  [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print(
        colored(
            f"  -  {data.get('current', {}).get('Time', 'N/A')} | Temp:  {data.get('current', {}).get('Temp', 'N/A')} | Feels:  {data.get('current', {}).get('Phrase', 'N/A')} | AQI (?)",
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


def print_daytime_forecast(data):
    """Print daytime forecast details."""
    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print(
        colored(
            f"  - Temp:  {data.get('day',  {}).get('Temp', 'N/A')} | Feels:  {data.get('day',  {}).get('Phrase', 'N/A')} | AQI  (?)",
            "yellow",
        )
    )
    print(
        colored(
            f"  - UV Index:  {data.get('day',  {}).get('Max UV Index', 'N/A')} | Wind:  {data.get('day',  {}).get('Wind', 'N/A')} | Gusts:  {data.get('day',  {}).get('Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f"  - Cloud Cover:  {data.get('day',  {}).get('Cloud Cover', 'N/A')} | Rain:  {data.get('day',  {}).get('Rain', 'N/A')} | Thunder:  {data.get('day',  {}).get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )


def print_nighttime_forecast(data):
    """Print nighttime forecast details."""
    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print(
        colored(
            f"  - Temp:  {data.get('night',  {}).get('Temp', 'N/A')} | Feels:  {data.get('night',  {}).get('Phrase', 'N/A')} | AQI  (?)",
            "yellow",
        )
    )
    print(
        colored(
            f"  - UV Index:  {data.get('night',  {}).get('Max UV Index', 'N/A')} | Wind:  {data.get('night',  {}).get('Wind', 'N/A')} | Gusts:  {data.get('night',  {}).get('Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f"  - Cloud Cover:  {data.get('night',  {}).get('Cloud Cover', 'N/A')} | Rain:  {data.get('night',  {}).get('Rain', 'N/A')} | Thunder:  {data.get('night',  {}).get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )


def print_forecast(data):
    """Print forecast details."""
    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print(
            colored(
                f"  -> {forecast[i+1].get('Date', 'N/A')} | {forecast[i+1].get('Temp',  {}).get('max', 'N/A')} >>>>> {forecast[i+1].get('Temp',  {}).get('min', 'N/A')}",
                "magenta",
            )
        )
        print(
            colored(
                "  " * 3
                + f"- Rain:  {forecast[i+1].get('Rain', 'N/A')} | Hours of Rain:  {forecast[i+1].get('Hours of Precipitation', 'N/A')} | Cloud Cover:  {forecast[i+1].get('Cloud Cover', 'N/A')}",
                "green",
            )
        )
        print(
            colored(
                "  " * 3
                + f"- Wind:  {forecast[i+1].get('Wind', ' N/A')[1:]} | Gusts:  {forecast[i+1].get('Wind Gusts', 'N/A')} | Thunder:  {forecast[i+1].get('Probability of Thunderstorms', 'N/A')}",
                "yellow",
            )
        )


def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    print_current_weather(data, city, country_code)
    print_daytime_forecast(data)
    print_nighttime_forecast(data)
    print_forecast(data)
    print(
        colored(
            "\n  "
            + "-" * 17
            + f"{colored(f'Powered by AccuWeather  ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}"
            + f"{colored('-' * 17, 'red')}",
            "green",
        )
    )


def run(data, city, country_code):
    """Prints the weather in data, timing from now. Public entry point of this unit."""
    return fmt_cli_resp(data, city, country_code, datetime.now())
