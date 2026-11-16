from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def fmt_cli_resp_header(city: str, country_code: str) -> str:
    """Format the weather data to CLI response header."""
    return colored(
        f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
        "green",
        attrs=["bold"],
    )


def fmt_cli_resp_current(data) -> str:
    """Format the current weather data to CLI response."""
    return colored(
        f" - {data.get('current', {}).get('Time', 'N/A')} | Temp: {data.get('current', {}).get('Temp', 'N/A')} | Feels: {data.get('current', {}).get('Phrase', 'N/A')} | AQI (?)",
        "red",
    )


def fmt_cli_resp_forecast(data) -> str:
    """Format the forecast weather data to CLI response."""
    return colored(
        f" - {data.get('date', 'N/A')} | {data.get('Temp', {}).get('max', 'N/A')} >>>>> {data.get('Temp', {}).get('min', 'N/A')}",
        "magenta",
    )


def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    start_time = datetime.now()
    print(fmt_cli_resp_header(cidade, codigo_pais))
    print(fmt_cli_resp_current(data.get('current', {})))
    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print(fmt_cli_resp_current(data.get('day', {})))
    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print(fmt_cli_resp_current(data.get('night', {})))
    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print(fmt_cli_resp_forecast(forecast[i+1]))
    print(
        colored(
            "\n "
            + "-" * 17
            + f"{colored(f'Powered by AccuWeather ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}"
            + f"{colored('-'* 17, 'red')}",
            "green",
        )
    )
