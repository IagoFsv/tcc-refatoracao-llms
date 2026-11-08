from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def format_weather_section(data, section_key, title_color, text_color):
    """Format a section of weather data."""
    print(colored(f"\n[{title_color}] {section_key.capitalize()}", text_color, attrs=["bold"]))
    for key, value in data.items():
        print(colored(f" - {key.title()}: {value if value else 'N/A'}", text_color))


def format_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    print(
        colored(
            f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    format_weather_section(data.get('current', {}), 'current', 'red', 'red')
    format_weather_section(data.get('day', {}), 'day', 'red', 'green')
    format_weather_section(data.get('night', {}), 'night', 'red', 'blue')

    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print(
            colored(
                f" -> {forecast[i].get('Date', 'N/A')} | {forecast[i].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[i].get('Temp', {}).get('min', 'N/A')}",
                "magenta",
            )
        )
        format_weather_section(forecast[i], 'forecast', 'green', 'green')

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
    return format_cli_resp(dados, cidade, codigo_pais, datetime.now())
