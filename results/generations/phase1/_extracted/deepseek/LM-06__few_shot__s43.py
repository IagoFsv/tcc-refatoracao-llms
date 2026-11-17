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
    print(
        colored(
            f"[*] Current Weather for  {city.capitalize()},  {country_code.upper()}  [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print_current_weather_details(data)


def print_current_weather_details(data):
    print(
        colored(
            f"  -  {data.get('current', {}).get('Time', 'N/A')} | Temp:  {data.get('current', {}).get('Temp', 'N/A')} | Feels:  {data.get('current', {}).get('Phrase', 'N/A')} | AQI (?)",
            "red",
        )
    )
    print_current_weather_details_extra(data)


def print_current_weather_details_extra(data):
    print(
        colored(
            f"  - RealFeel Sun:  {data.get('current', {}).get('Realfeel sun', 'N/A')} | RealFeel Shade:  {data.get('current', {}).get('Realfeel shade', 'N/A')} | UV Index:  {data.get('current', {}).get('Max uv index', 'N/A')}",
            "blue",
        )
    )
    print_current_weather_details_extra_2(data)


def print_current_weather_details_extra_2(data):
    print(
        colored(
            f"  - Wind:  {data.get('current', {}).get('Wind', ' N/A')[1:]} | Gusts:  {data.get('current', {}).get('Wind gusts', 'N/A')} | Cloud Cover:  {data.get('current', {}).get('Cloud cover', 'N/A')}",
            "green",
        )
    )
    print_current_weather_details_extra_3(data)


def print_current_weather_details_extra_3(data):
    print(
        colored(
            f"  - Dew Point:  {data.get('current', {}).get('Dew point', 'N/A')} | Humidity:  {data.get('current', {}).get('Humidity', 'N/A')} | Indoor Humidity:  {data.get('current', {}).get('Indoor humidity', 'N/A')}",
            "cyan",
        )
    )
    print_current_weather_details_extra_4(data)


def print_current_weather_details_extra_4(data):
    print(
        colored(
            f"  - Visibility:  {data.get('current', {}).get('Visibility', 'N/A')} | Pressure:  {data.get('current', {}).get('Pressure', 'N/A')} | Ceiling:  {data.get('current', {}).get('Cloud ceiling', 'N/A')}",
            "yellow",
        )
    )


def print_forecast(data, time_of_day):
    print(colored(f"\n[*] {time_of_day} Forecast", "red", attrs=["bold"]))
    print_forecast_details(data, time_of_day)


def print_forecast_details(data, time_of_day):
    print(
        colored(
            f"  - Temp:  {data.get(time_of_day, {}).get('Temp', 'N/A')} | Feels:  {data.get(time_of_day, {}).get('Phrase', 'N/A')} | AQI (?)",
            "yellow",
        )
    )
    print_forecast_details_extra(data, time_of_day)


def print_forecast_details_extra(data, time_of_day):
    print(
        colored(
            f"  - UV Index:  {data.get(time_of_day, {}).get('Max UV Index', 'N/A')} | Wind:  {data.get(time_of_day, {}).get('Wind', 'N/A')} | Gusts:  {data.get(time_of_day, {}).get('Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print_forecast_details_extra_2(data, time_of_day)


def print_forecast_details_extra_2(data, time_of_day):
    print(
        colored(
            f"  - Cloud Cover:  {data.get(time_of_day, {}).get('Cloud Cover', 'N/A')} | Rain:  {data.get(time_of_day, {}).get('Rain', 'N/A')} | Thunder:  {data.get(time_of_day, {}).get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )


def print_forecast_next_5_days(data):
    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print_forecast_next_5_days_details(forecast, i + 1)


def print_forecast_next_5_days_details(forecast, day):
    print(
        colored(
            f"  -> {forecast[day].get('Date', 'N/A')} | {forecast[day].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[day].get('Temp', {}).get('min', 'N/A')}",
            "magenta",
        )
    )
    print_forecast_next_5_days_details_extra(forecast, day)


def print_forecast_next_5_days_details_extra(forecast, day):
    print(
        colored(
            "  " * 3
            + f"- Rain:  {forecast[day].get('Rain', 'N/A')} | Hours of Rain:  {forecast[day].get('Hours of Precipitation', 'N/A')} | Cloud Cover:  {forecast[day].get('Cloud Cover', 'N/A')}",
            "green",
        )
    )
    print_forecast_next_5_days_details_extra_2(forecast, day)


def print_forecast_next_5_days_details_extra_2(forecast, day):
    print(
        colored(
            "  " * 3
            + f"- Wind:  {forecast[day].get('Wind', ' N/A')[1:]} | Gusts:  {forecast[day].get('Wind Gusts', 'N/A')} | Thunder:  {forecast[day].get('Probability of Thunderstorms', 'N/A')}",
            "yellow",
        )
    )


def print_powered_by(start_time):
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
