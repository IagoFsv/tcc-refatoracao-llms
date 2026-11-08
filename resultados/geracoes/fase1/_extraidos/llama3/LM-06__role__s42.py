from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def fmt_cli_resp_header(city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response header."""
    return colored(
        f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
        "green",
        attrs=["bold"],
    )


def fmt_cli_resp_current(data: dict) -> str:
    """Format the current weather data to CLI response."""
    return colored(
        f" - {data.get('current', {}).get('Time', 'N/A')} | Temp: {data.get('current', {}).get('Temp', 'N/A')} | Feels: {data.get('current', {}).get('Phrase', 'N/A')} | AQI (?)",
        "red",
    )


def fmt_cli_resp_forecast(data: dict) -> str:
    """Format the forecast weather data to CLI response."""
    return colored(
        f" - Temp: {data.get('Temp', 'N/A')} | Feels: {data.get('Phrase', 'N/A')} | AQI (?)",
        "yellow",
    )


def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    return fmt_cli_resp(
        dados, cidade, codigo_pais, datetime.now()
    )
