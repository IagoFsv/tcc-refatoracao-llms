from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def format_weather(current_weather):
    """Format a single weather entry for CLI response."""
    return colored(
        f" - {current_weather.get('Time', 'N/A')} | Temp: {current_weather.get('Temp', 'N/A')} | Feels: {current_weather.get('Phrase', 'N/A')} | AQI (?)",
        "red",
    )


def format_forecast(day_weather):
    """Format a single day forecast entry for CLI response."""
    return colored(
        f" - Temp: {day_weather.get('Temp', 'N/A')} | Feels: {day_weather.get('Phrase', 'N/A')} | AQI (?)",
        "yellow",
    )


def format_night_weather(night_weather):
    """Format a single night forecast entry for CLI response."""
    return colored(
        f" - Temp: {night_weather.get('Temp', 'N/A')} | Feels: {night_weather.get('Phrase', 'N/A')} | AQI (?)",
        "yellow",
    )


def format_forecast_entry(forecast_entry):
    """Format a single forecast entry for CLI response."""
    return colored(
        f" -> {forecast_entry.get('Date', 'N/A')} | {forecast_entry.get('Temp', {}).get('max', 'N/A')} >>>>> {forecast_entry.get('Temp', {}).get('min', 'N/A')}",
        "magenta",
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
    print(
        colored(
            f" - {data.get('current', {}).get('Time', 'N/A')} | Temp: {data.get('current', {}).get('Temp', 'N/A')} | Feels: {data.get('current', {}).get('Phrase', 'N/A')} | AQI (?)",
            "red",
        )
    )
    print(
        colored(
            f" - RealFeel Sun: {data.get('current', {}).get('Realfeel sun', 'N/A')} | RealFeel Shade: {data.get('current', {}).get('Realfeel shade', 'N/A')} | UV Index: {data.get('current', {}).get('Max uv index', 'N/A')}",
            "blue",
        )
    )
    print(
        colored(
            f" - Wind: {data.get('current', {}).get('Wind', ' N/A')[1:]} | Gusts: {data.get('current', {}).get('Wind gusts', 'N/A')} | Cloud Cover: {data.get('current', {}).get('Cloud cover', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Dew Point: {data.get('current', {}).get('Dew point', 'N/A')} | Humidity: {data.get('current', {}).get('Humidity', 'N/A')} | Indoor Humidity: {data.get('current', {}).get('Indoor humidity', 'N/A')}",
            "cyan",
        )
    )
    print(
        colored(
            f" - Visibility: {data.get('current', {}).get('Visibility', 'N/A')} | Pressure: {data.get('current', {}).get('Pressure', 'N/A')} | Ceiling: {data.get('current', {}).get('Cloud ceiling', 'N/A')}",
            "yellow",
        )
    )

    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print(format_weather(data.get('day', {})))
    print(
        colored(
            f" - UV Index: {data.get('day', {}).get('Max UV Index', 'N/A')} | Wind: {data.get('day', {}).get('Wind', 'N/A')} | Gusts: {data.get('day', {}).get('Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Cloud Cover: {data.get('day', {}).get('Cloud Cover', 'N/A')} | Rain: {data.get('day', {}).get('Rain', 'N/A')} | Thunder: {data.get('day', {}).get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )

    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print(format_weather(data.get('night', {})))
    print(
        colored(
            f" - UV Index: {data.get('night', {}).get('Max UV Index', 'N/A')} | Wind: {data.get('night', {}).get('Wind', 'N/A')} | Gusts: {data.get('night', {}).get('Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Cloud Cover: {data.get('night', {}).get('Cloud Cover', 'N/A')} | Rain: {data.get('night', {}).get('Rain', 'N/A')} | Thunder: {data.get('night', {}).get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )

    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print(format_forecast_entry(forecast[i+1]))
        print(
            colored(
                " " * 3
                + f"- Rain: {forecast[i+1].get('Rain', 'N/A')} | Hours of Rain: {forecast[i+1].get('Hours of Precipitation', 'N/A')} | Cloud Cover: {forecast[i+1].get('Cloud Cover', 'N/A')}",
                "green",
            )
        )
        print(
            colored(
                " " * 3
                + f"- Wind: {forecast[i+1].get('Wind', ' N/A')[1:]} | Gusts: {forecast[i+1].get('Wind Gusts', 'N/A')} | Thunder: {forecast[i+1].get('Probability of Thunderstorms', 'N/A')}",
                "yellow",
            )
        )
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
