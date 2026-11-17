"""Command-line response with the current weather and the forecast.

Public entry point: run(data, city, country_code). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a,  %d-%b-%y")


def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    print_current_weather(data, city, country_code)
    print_forecast(data, "DayTime")
    print_forecast(data, "NightTime")
    print_forecast_next_5_days(data)
    print_powered_by(start_time)


def print_current_weather(data, city, country_code):
    """Print current weather data."""
    print(
        colored(
            f"[*] Current Weather for  {city.capitalize()},  {country_code.upper()}  [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print_weather_details(data, "current")


def print_weather_details(data, weather_type):
    """Print weather details."""
    print(
        colored(
            f"  -  {data.get(weather_type,  {}).get('Time',  'N/A')} | Temp:  {data.get(weather_type,  {}).get('Temp',  'N/A')} | Feels:  {data.get(weather_type,  {}).get('Phrase',  'N/A')} | AQI  (?)",
            "red",
        )
    )
    print(
        colored(
            f"  - RealFeel Sun:  {data.get(weather_type,  {}).get('Realfeel sun',  'N/A')} | RealFeel Shade:  {data.get(weather_type,  {}).get('Realfeel shade',  'N/A')} | UV Index:  {data.get(weather_type,  {}).get('Max uv index',  'N/A')}",
            "blue",
        )
    )
    print(
        colored(
            f"  - Wind:  {data.get(weather_type,  {}).get('Wind',  ' N/A')[1:]} | Gusts:  {data.get(weather_type,  {}).get('Wind gusts',  'N/A')} | Cloud Cover:  {data.get(weather_type,  {}).get('Cloud cover',  'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f"  - Dew Point:  {data.get(weather_type,  {}).get('Dew point',  'N/A')} | Humidity:  {data.get(weather_type,  {}).get('Humidity',  'N/A')} | Indoor Humidity:  {data.get(weather_type,  {}).get('Indoor humidity',  'N/A')}",
            "cyan",
        )
    )
    print(
        colored(
            f"  - Visibility:  {data.get(weather_type,  {}).get('Visibility',  'N/A')} | Pressure:  {data.get(weather_type,  {}).get('Pressure',  'N/A')} | Ceiling:  {data.get(weather_type,  {}).get('Cloud ceiling',  'N/A')}",
            "yellow",
        )
    )


def print_forecast(data, forecast_type):
    """Print forecast data."""
    print(colored(f"[*] {forecast_type} Forecast", "red", attrs=["bold"]))
    print_weather_details(data, forecast_type)


def print_forecast_next_5_days(data):
    """Print forecast for next 5 days."""
    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print(
            colored(
                f"  -> {forecast[i+1].get('Date',  'N/A')} | {forecast[i+1].get('Temp',  {}).get('max',  'N/A')} >>>>> {forecast[i+1].get('Temp',  {}).get('min',  'N/A')}",
                "magenta",
            )
        )
        print_forecast_details(forecast, i+1)


def print_forecast_details(forecast, index):
    """Print forecast details."""
    print(
        colored(
            "  " * 3
            + f"- Rain:  {forecast[index].get('Rain',  'N/A')} | Hours of Rain:  {forecast[index].get('Hours of Precipitation',  'N/A')} | Cloud Cover:  {forecast[index].get('Cloud Cover',  'N/A')}",
            "green",
        )
    )
    print(
        colored(
            "  " * 3
            + f"- Wind:  {forecast[index].get('Wind',  ' N/A')[1:]} | Gusts:  {forecast[index].get('Wind Gusts',  'N/A')} | Thunder:  {forecast[index].get('Probability of Thunderstorms',  'N/A')}",
            "yellow",
        )
    )


def print_powered_by(start_time):
    """Print powered by message."""
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
