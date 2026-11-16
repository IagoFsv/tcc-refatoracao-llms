"""Resposta de linha de comando com o clima atual e a previsao.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a,  %d-%b-%y")


def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    print_weather_data(data, city, country_code, start_time)


def print_weather_data(data, city: str, country_code: str, start_time: datetime):
    """Print the weather data."""
    print_current_weather(data, city, country_code, start_time)
    print_day_time_forecast(data)
    print_night_time_forecast(data)
    print_forecast_for_next_5_days(data)


def print_current_weather(data, city: str, country_code: str, start_time: datetime):
    """Print current weather data."""
    print(
        colored(
            f"[*] Current Weather for  {city.capitalize()},  {country_code.upper()}  [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print_current_weather_details(data)


def print_current_weather_details(data):
    """Print current weather details."""
    print(
        colored(
            f"  -  {data.get('current', {}).get('Time', 'N/A')}  Temp:  {data.get('current', {}).get('Temp', 'N/A')}  Feels:  {data.get('current', {}).get('Phrase', 'N/A')}  AQI  (?)",
            "red",
        )
    )
    print_current_weather_details_additional(data)


def print_current_weather_details_additional(data):
    """Print additional current weather details."""
    print(
        colored(
            f"  - RealFeel Sun:  {data.get('current', {}).get('Realfeel sun', 'N/A')}  RealFeel Shade:  {data.get('current', {}).get('Realfeel shade', 'N/A')}  UV Index:  {data.get('current', {}).get('Max uv index', 'N/A')}",
            "blue",
        )
    )
    print_current_weather_details_additional_more(data)


def print_current_weather_details_additional_more(data):
    """Print more additional current weather details."""
    print(
        colored(
            f"  - Wind:  {data.get('current', {}).get('Wind', ' N/A')[1:]}  Gusts:  {data.get('current', {}).get('Wind gusts', 'N/A')}  Cloud Cover:  {data.get('current', {}).get('Cloud cover', 'N/A')}",
            "green",
        )
    )
    print_current_weather_details_additional_more_more(data)


def print_current_weather_details_additional_more_more(data):
    """Print more more additional current weather details."""
    print(
        colored(
            f"  - Dew Point:  {data.get('current', {}).get('Dew point', 'N/A')}  Humidity:  {data.get('current', {}).get('Humidity', 'N/A')}  Indoor Humidity:  {data.get('current', {}).get('Indoor humidity', 'N/A')}",
            "cyan",
        )
    )
    print_current_weather_details_additional_more_more_more(data)


def print_current_weather_details_additional_more_more_more(data):
    """Print more more more additional current weather details."""
    print(
        colored(
            f"  - Visibility:  {data.get('current', {}).get('Visibility', 'N/A')}  Pressure:  {data.get('current', {}).get('Pressure', 'N/A')}  Ceiling:  {data.get('current', {}).get('Cloud ceiling', 'N/A')}",
            "yellow",
        )
    )


def print_day_time_forecast(data):
    """Print day time forecast."""
    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print_day_time_forecast_details(data)


def print_day_time_forecast_details(data):
    """Print day time forecast details."""
    print(
        colored(
            f"  - Temp:  {data.get('day', {}).get('Temp', 'N/A')}  Feels:  {data.get('day', {}).get('Phrase', 'N/A')}  AQI  (?)",
            "yellow",
        )
    )
    print_day_time_forecast_details_additional(data)


def print_day_time_forecast_details_additional(data):
    """Print additional day time forecast details."""
    print(
        colored(
            f"  - UV Index:  {data.get('day', {}).get('Max UV Index', 'N/A')}  Wind:  {data.get('day', {}).get('Wind', 'N/A')}  Gusts:  {data.get('day', {}).get('Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print_day_time_forecast_details_additional_more(data)


def print_day_time_forecast_details_additional_more(data):
    """Print more additional day time forecast details."""
    print(
        colored(
            f"  - Cloud Cover:  {data.get('day', {}).get('Cloud Cover', 'N/A')}  Rain:  {data.get('day', {}).get('Rain', 'N/A')}  Thunder:  {data.get('day', {}).get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )


def print_night_time_forecast(data):
    """Print night time forecast."""
    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print_night_time_forecast_details(data)


def print_night_time_forecast_details(data):
    """Print night time forecast details."""
    print(
        colored(
            f"  - Temp:  {data.get('night', {}).get('Temp', 'N/A')}  Feels:  {data.get('night', {}).get('Phrase', 'N/A')}  AQI  (?)",
            "yellow",
        )
    )
    print_night_time_forecast_details_additional(data)


def print_night_time_forecast_details_additional(data):
    """Print additional night time forecast details."""
    print(
        colored(
            f"  - UV Index:  {data.get('night', {}).get('Max UV Index', 'N/A')}  Wind:  {data.get('night', {}).get('Wind', 'N/A')}  Gusts:  {data.get('night', {}).get('Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print_night_time_forecast_details_additional_more(data)


def print_night_time_forecast_details_additional_more(data):
    """Print more additional night time forecast details."""
    print(
        colored(
            f"  - Cloud Cover:  {data.get('night', {}).get('Cloud Cover', 'N/A')}  Rain:  {data.get('night', {}).get('Rain', 'N/A')}  Thunder:  {data.get('night', {}).get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )


def print_forecast_for_next_5_days(data):
    """Print forecast for next 5 days."""
    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print_forecast_for_next_5_days_details(forecast, i)
    print_forecast_for_next_5_days_footer(data, start_time)


def print_forecast_for_next_5_days_details(forecast, i):
    """Print forecast for next 5 days details."""
    print(
        colored(
            f"  -> {forecast[i+1].get('Date', 'N/A')}  {forecast[i+1].get('Temp', {}).get('max', 'N/A')} >> {forecast[i+1].get('Temp', {}).get('min', 'N/A')}",
            "magenta",
        )
    )
    print_forecast_for_next_5_days_details_additional(forecast, i)


def print_forecast_for_next_5_days_details_additional(forecast, i):
    """Print additional forecast for next 5 days details."""
    print(
        colored(
            "  " * 3
            + f"- Rain:  {forecast[i+1].get('Rain', 'N/A')}  Hours of Rain:  {forecast[i+1].get('Hours of Precipitation', 'N/A')}  Cloud Cover:  {forecast[i+1].get('Cloud Cover', 'N/A')}",
            "green",
        )
    )
    print_forecast_for_next_5_days_details_additional_more(forecast, i)


def print_forecast_for_next_5_days_details_additional_more(forecast, i):
    """Print more additional forecast for next 5 days details."""
    print(
        colored(
            "  " * 3
            + f"- Wind:  {forecast[i+1].get('Wind', ' N/A')[1:]}  Gusts:  {forecast[i+1].get('Wind Gusts', 'N/A')}  Thunder:  {forecast[i+1].get('Probability of Thunderstorms', 'N/A')}",
            "yellow",
        )
    )


def print_forecast_for_next_5_days_footer(data, start_time):
    """Print footer for forecast for next 5 days."""
    print(
        colored(
            "\n  "
            + "-" * 17
            + f"{colored(f'Powered by AccuWeather  ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}"
            + f"{colored('-' * 17, 'red')}",
            "green",
        )
    )


def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    return fmt_cli_resp(dados, cidade, codigo_pais, datetime.now())
