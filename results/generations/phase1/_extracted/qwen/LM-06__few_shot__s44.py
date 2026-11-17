"""Command-line response with the current weather and the forecast.

Public entry point: run(data, city, country_code). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def _format_weather(data, weather_type):
    return f" - {data.get(weather_type, {}).get('Temp', 'N/A')} | Feels: {data.get(weather_type, {}).get('Phrase', 'N/A')} | AQI (?)"


def _format_uv_wind(data, weather_type):
    return f" - UV Index: {data.get(weather_type, {}).get('Max UV Index', 'N/A')} | Wind: {data.get(weather_type, {}).get('Wind', 'N/A')} | Gusts: {data.get(weather_type, {}).get('Wind Gusts', 'N/A')}"


def _format_cloud_rain(data, weather_type):
    return f" - Cloud Cover: {data.get(weather_type, {}).get('Cloud Cover', 'N/A')} | Rain: {data.get(weather_type, {}).get('Rain', 'N/A')} | Thunder: {data.get(weather_type, {}).get('Probability of Thunderstorms', 'N/A')}"


def _format_forecast(forecast, i):
    return (
        f" -> {forecast[i+1].get('Date', 'N/A')} | {forecast[i+1].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[i+1].get('Temp', {}).get('min', 'N/A')}"
        f"\n {colored(' ' * 3 + f'- Rain: {forecast[i+1].get('Rain', 'N/A')} | Hours of Rain: {forecast[i+1].get('Hours of Precipitation', 'N/A')} | Cloud Cover: {forecast[i+1].get('Cloud Cover', 'N/A')}", 'green')}"
        f"\n {colored(' ' * 3 + f'- Wind: {forecast[i+1].get('Wind', ' N/A')[1:]} | Gusts: {forecast[i+1].get('Wind Gusts', 'N/A')} | Thunder: {forecast[i+1].get('Probability of Thunderstorms', 'N/A')}", 'yellow')}"
    )


def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    print(
        colored(
            f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print(colored(_format_weather(data, 'current'), "red"))
    print(colored(_format_uv_wind(data, 'current'), "blue"))
    print(colored(_format_cloud_rain(data, 'current'), "green"))
    print(colored(_format_cloud_rain(data, 'current'), "cyan"))
    print(colored(_format_cloud_rain(data, 'current'), "yellow"))

    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print(colored(_format_weather(data, 'day'), "yellow"))
    print(colored(_format_uv_wind(data, 'day'), "green"))
    print(colored(_format_cloud_rain(data, 'day'), "blue"))

    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print(colored(_format_weather(data, 'night'), "yellow"))
    print(colored(_format_uv_wind(data, 'night'), "green"))
    print(colored(_format_cloud_rain(data, 'night'), "blue"))

    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print(colored(_format_forecast(forecast, i), "magenta"))

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
