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
    print_current_weather(data, city, country_code, start_time)
    print_day_forecast(data)
    print_night_forecast(data)
    print_forecast_next_5_days(data)


def print_current_weather(data, city, country_code, start_time):
    """Prints the current weather for given city and country."""
    print(colored(f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{get_current_date()}]", "green", attrs=["bold"]))
    print_weather_details(data, 'current')


def print_weather_details(data, time):
    """Prints the weather details for given time (current/day/night)."""
    print(colored(f"  - {data.get(time, {}).get('Time', 'N/A')} | Temp: {data.get(time, {}).get('Temp', 'N/A')} | Feels: {data.get(time, {}).get('Phrase', 'N/A')} | AQI  (?)", "red"))
    print(colored(f"  - RealFeel Sun: {data.get(time, {}).get('Realfeel sun', 'N/A')} | RealFeel Shade: {data.get(time, {}).get('Realfeel shade', 'N/A')} | UV Index: {data.get(time, {}).get('Max uv index', 'N/A')}", "blue"))
    print(colored(f"  - Wind: {data.get(time, {}).get('Wind', ' N/A')[1:]} | Gusts: {data.get(time, {}).get('Wind gusts', 'N/A')} | Cloud Cover: {data.get(time, {}).get('Cloud cover', 'N/A')}", "green"))
    print(colored(f"  - Dew Point: {data.get(time, {}).get('Dew point', 'N/A')} | Humidity: {data.get(time, {}).get('Humidity', 'N/A')} | Indoor Humidity: {data.get(time, {}).get('Indoor humidity', 'N/A')}", "cyan"))
    print(colored(f"  - Visibility: {data.get(time, {}).get('Visibility', 'N/A')} | Pressure: {data.get(time, {}).get('Pressure', 'N/A')} | Ceiling: {data.get(time, {}).get('Cloud ceiling', 'N/A')}", "yellow"))


def print_day_forecast(data):
    """Prints the day forecast."""
    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print_weather_details(data, 'day')


def print_night_forecast(data):
    """Prints the night forecast."""
    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print_weather_details(data, 'night')


def print_forecast_next_5_days(data):
    """Prints the forecast for next 5 days."""
    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print(colored(f"  -> {forecast[i+1].get('Date', 'N/A')} | {forecast[i+1].get('Temp', {}).get('max', 'N/A')} 
        >>>>> {forecast[i+1].get('Temp', {}).get('min', 'N/A')}", "magenta"))
        print(colored(f"  - Rain: {forecast[i+1].get('Rain', 'N/A')} | Hours of Rain: {forecast[i+1].get('Hours of Precipitation', 'N/A')} | Cloud Cover: {forecast[i+1].get('Cloud Cover', 'N/A')}", "green"))
        print(colored(f"  - Wind: {forecast[i+1].get('Wind', ' N/A')[1:]} | Gusts: {forecast[i+1].get('Wind Gusts', 'N/A')} | Thunder: {forecast[i+1].get('Probability of Thunderstorms', 'N/A')}", "yellow"))
    print(colored(f"\n {'-'*17}Powered by AccuWeather  ({round((datetime.now() - start_time).total_seconds(), 2)}s){'-'*17}", "green"))


def run(data, city, country_code):
    """Prints the weather in data, timing from now. Public entry point of this unit."""
    return fmt_cli_resp(data, city, country_code, datetime.now())
