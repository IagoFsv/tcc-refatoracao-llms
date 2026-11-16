from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    print(
        colored(
            f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print_weather_details(data, "current")
    print_weather_details(data, "day")
    print_weather_details(data, "night")
    print_forecast(data, "forecast")
    print_powered_by(start_time)


def print_weather_details(data, time_of_day: str):
    """Print weather details for a given time of day."""
    details = data.get(time_of_day, {})
    print(
        colored(
            f" - Temp: {details.get('Temp', 'N/A')} | Feels: {details.get('Phrase', 'N/A')} | AQI (?)",
            "red",
        )
    )
    print(
        colored(
            f" - UV Index: {details.get(f'Max {time_of_day.capitalize()} UV Index', 'N/A')} | Wind: {details.get('Wind', 'N/A')} | Gusts: {details.get(f'Wind Gusts', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Cloud Cover: {details.get(f'Cloud Cover', 'N/A')} | Rain: {details.get('Rain', 'N/A')} | Thunder: {details.get(f'Probability of {time_of_day.capitalize()} Thunderstorms', 'N/A')}",
            "blue",
        )
    )


def print_forecast(data, forecast_key: str):
    """Print forecast details."""
    forecast = data.get(forecast_key, [])
    for i in range(5):
        print(
            colored(
                f" -> {forecast[i].get('Date', 'N/A')} | {forecast[i].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[i].get('Temp', {}).get('min', 'N/A')}",
                "magenta",
            )
        )
        print(
            colored(
                " " * 3
                + f"- Rain: {forecast[i].get('Rain', 'N/A')} | Hours of Rain: {forecast[i].get('Hours of Precipitation', 'N/A')} | Cloud Cover: {forecast[i].get('Cloud Cover', 'N/A')}",
                "green",
            )
        )
        print(
            colored(
                " " * 3
                + f"- Wind: {forecast[i].get('Wind', ' N/A')[1:]} | Gusts: {forecast[i].get('Wind Gusts', 'N/A')} | Thunder: {forecast[i].get(f'Probability of {forecast_key.capitalize()} Thunderstorms', 'N/A')}",
                "yellow",
            )
        )


def print_powered_by(start_time: datetime):
    """Print powered by information."""
    print(
        colored(
            "\n "
            + "-" * 17
            + f"{colored(f'Powered by AccuWeather ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}"
            + f"{colored('-'* 17, 'red')}",
            "green",
        )
    )


def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    return fmt_cli_resp(dados, cidade, codigo_pais, datetime.now())
