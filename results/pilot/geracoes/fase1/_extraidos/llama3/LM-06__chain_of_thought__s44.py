from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def print_current_weather(data, city, country_code, start_time):
    """Print current weather data."""
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
    # ...

def print_forecast(data, start_time):
    """Print forecast data."""
    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    # ...
    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    # ...
    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    # ...

def fmt_cli_resp(data, city, country_code, start_time):
    """Format the weather data to CLI response."""
    print_current_weather(data, city, country_code, start_time)
    print_forecast(data, start_time)
    # ...

def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    return fmt_cli_resp(dados, cidade, codigo_pais, datetime.now())
