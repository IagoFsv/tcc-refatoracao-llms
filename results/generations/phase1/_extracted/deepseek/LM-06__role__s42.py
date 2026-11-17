"""Command-line response with the current weather and the forecast.

Public entry point: run(data, city, country_code). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a,  %d-%b-%y")


def fmt_current_weather(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    current_weather_data = data.get('current', {})
    return (
        f"[*] Current Weather for  {city.capitalize()},  {country_code.upper()}  [{get_current_date()}]",
        f"  -  {current_weather_data.get('Time',  'N/A')} | Temp:  {current_weather_data.get('Temp',  'N/A')} | Feels:  {current_weather_data.get('Phrase',  'N/A')} | AQI (?)",
        f"  - RealFeel Sun:  {current_weather_data.get('Realfeel sun',  'N/A')} | RealFeel Shade:  {current_weather_data.get('Realfeel shade',  'N/A')} | UV Index:  {current_weather_data.get('Max uv index',  'N/A')}",
        f"  - Wind:  {current_weather_data.get('Wind',  ' N/A')[1:]} | Gusts:  {current_weather_data.get('Wind gusts',  'N/A')} | Cloud Cover:  {current_weather_data.get('Cloud cover',  'N/A')}",
        f"  - Dew Point:  {current_weather_data.get('Dew point',  'N/A')} | Humidity:  {current_weather_data.get('Humidity',  'N/A')} | Indoor Humidity:  {current_weather_data.get('Indoor humidity',  'N/A')}",
        f"  - Visibility:  {current_weather_data.get('Visibility',  'N/A')} | Pressure:  {current_weather_data.get('Pressure',  'N/A')} | Ceiling:  {current_weather_data.get('Cloud ceiling',  'N/A')}",
    )

def fmt_forecast_day_night(data, forecast_type: str):
    """Format the forecast data to CLI response."""
    forecast_data = data.get(forecast_type, {})
    return (
        f"  - Temp:  {forecast_data.get('Temp',  'N/A')} | Feels:  {forecast_data.get('Phrase',  'N/A')} | AQI (?)",
        f"  - UV Index:  {forecast_data.get('Max UV Index',  'N/A')} | Wind:  {forecast_data.get('Wind',  'N/A')} | Gusts:  {forecast_data.get('Wind Gusts',  'N/A')}",
        f"  - Cloud Cover:  {forecast_data.get('Cloud Cover',  'N/A')} | Rain:  {forecast_data.get('Rain',  'N/A')} | Thunder:  {forecast_data.get('Probability of Thunderstorms',  'N/A')}",
    )

def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    current_weather_data = fmt_current_weather(data, city, country_code, start_time)
    day_forecast_data = fmt_forecast_day_night(data, "day")
    night_forecast_data = fmt_forecast_day_night(data, "night")
    forecast = data.get("forecast", [])

    print("\n".join([colored(data, "red") for data in current_weather_data]))
    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print("\n".join([colored(data, "yellow") for data in day_forecast_data]))
    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print("\n".join([colored(data, "blue") for data in night_forecast_data]))

    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    for i in range(5):
        forecast_data = forecast[i+1]
        print(
            colored(
                f"  -> {forecast_data.get('Date',  'N/A')} | {forecast_data.get('Temp',  {}).get('max',  'N/A')} >>>>> {forecast_data.get('Temp',  {}).get('min',  'N/A')}",
                 "magenta",
             )
        )
        print(
            colored(
                 "  " * 3
                + f"- Rain:  {forecast_data.get('Rain',  'N/A')} | Hours of Rain:  {forecast_data.get('Hours of Precipitation',  'N/A')} | Cloud Cover:  {forecast_data.get('Cloud Cover',  'N/A')}",
                 "green",
             )
        )
        print(
            colored(
                 "  " * 3
                + f"- Wind:  {forecast_data.get('Wind',  ' N/A')[1:]} | Gusts:  {forecast_data.get('Wind Gusts',  'N/A')} | Thunder:  {forecast_data.get('Probability of Thunderstorms',  'N/A')}",
                 "yellow",
             )
        )
    print(
        colored(
             "\n "
            + "-" * 17
            + f"{colored(f'Powered by AccuWeather  ({round((datetime.now()  - start_time).total_seconds(), 2)}s)',  'yellow')}"
            + f"{colored('-' * 17,  'red')}",
             "green",
         )
    )


def run(data, city, country_code):
    """Prints the weather in data, timing from now. Public entry point of this unit."""
    return fmt_cli_resp(data, city, country_code, datetime.now())
