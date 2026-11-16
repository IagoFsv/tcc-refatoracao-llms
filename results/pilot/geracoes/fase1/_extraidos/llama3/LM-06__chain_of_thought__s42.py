from termcolor import colored
from datetime import datetime

def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")

def print_current_weather(data, city, country_code):
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
    # ... (rest of the current weather data)

def print_forecast(data, city, country_code):
    """Print forecast data."""
    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    # ... (rest of the forecast data)

def print_powers_by_accuweather(start_time):
    """Print the 'Powered by AccuWeather' message with the execution time."""
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
    start_time = datetime.now()
    fmt_cli_resp(dados, cidade, codigo_pais, start_time)
    print_powers_by_accuweather(start_time)
