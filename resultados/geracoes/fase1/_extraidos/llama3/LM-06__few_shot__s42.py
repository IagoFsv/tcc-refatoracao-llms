from termcolor import colored
from datetime import datetime


def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    print(
        colored(
            f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print_current_weather(data.get('current', {}))

    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print_daytime_forecast(data.get('day', {}))

    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print_nighttime_forecast(data.get('night', {}))

    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print_forecast(forecast[i+1])

    print(
        colored(
            "\n "
            + "-" * 17
            + f"{colored(f'Powered by AccuWeather ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}"
            + f"{colored('-'* 17, 'red')}",
            "green",
        )
    )


def print_current_weather(current):
    print(
        colored(
            f" - {current.get('Time', 'N/A')} | Temp: {current.get('Temp', 'N/A')} | Feels: {current.get('Phrase', 'N/A')} | AQI (?)",
            "red",
        )
    )
    print(
        colored(
            f" - RealFeel Sun: {current.get('Realfeel sun', 'N/A')} | RealFeel Shade: {current.get('Realfeel shade', 'N/A')} | UV Index: {current.get('Max uv index', 'N/A')}",
            "blue",
        )
    )
    print(
        colored(
            f" - Wind: {current.get('Wind', ' N/A')[1:]} | Gusts: {current.get('Wind gusts', 'N/A')} | Cloud Cover: {current.get('Cloud cover', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Dew Point: {current.get('Dew point', 'N/A')} | Humidity: {current.get('Humidity', 'N/A')} | Indoor Humidity: {current.get('Indoor humidity', 'N/A')}",
            "cyan",
        )
    )
    print(
        colored(
            f" - Visibility: {current.get('Visibility', 'N/A')} | Pressure: {current.get('Pressure', 'N/A')} | Ceiling: {current.get('Cloud ceiling', 'N/A')}",
            "yellow",
        )
    )


def print_daytime_forecast(day):
    print(
        colored(
            f" - Temp: {day.get('Temp', 'N/A')} | Feels: {day.get('Phrase', 'N/A')} | AQI (?)",
            "yellow",
        )
    )
    print(
        colored(
            f" - UV Index: {day.get('Max UV Index', 'N/A')} | Wind: {day.get('Wind', 'N/A')} | Gusts: {day.get('Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Cloud Cover: {day.get('Cloud Cover', 'N/A')} | Rain: {day.get('Rain', 'N/A')} | Thunder: {day.get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )


def print_nighttime_forecast(night):
    print(
        colored(
            f" - Temp: {night.get('Temp', 'N/A')} | Feels: {night.get('Phrase', 'N/A')} | AQI (?)",
            "yellow",
        )
    )
    print(
        colored(
            f" - UV Index: {night.get('Max UV Index', 'N/A')} | Wind: {night.get('Wind', 'N/A')} | Gusts: {night.get('Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Cloud Cover: {night.get('Cloud Cover', 'N/A')} | Rain: {night.get('Rain', 'N/A')} | Thunder: {night.get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )


def print_forecast(forecast):
    print(
        colored(
            f" -> {forecast.get('Date', 'N/A')} | {forecast.get('Temp', {}).get('max', 'N/A')} >>>>> {forecast.get('Temp', {}).get('min', 'N/A')}",
            "magenta",
        )
    )
    print(
        colored(
            " " * 3
            + f"- Rain: {forecast.get('Rain', 'N/A')} | Hours of Rain: {forecast.get('Hours of Precipitation', 'N/A')} | Cloud Cover: {forecast.get('Cloud Cover', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            " " * 3
            + f"- Wind: {forecast.get('Wind', ' N/A')[1:]} | Gusts: {forecast.get('Wind Gusts', 'N/A')} | Thunder: {forecast.get('Probability of Thunderstorms', 'N/A')}",
            "yellow",
        )
    )


def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    return fmt_cli_resp(dados, cidade, codigo_pais, datetime.now())
