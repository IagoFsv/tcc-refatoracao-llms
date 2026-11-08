from termcolor import colored
from datetime import datetime

def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a,  %d-%b-%y")

def print_current_weather(data, city: str, country_code: str):
    """Print the current weather data."""
    print(
        colored(
            f"[*] Current Weather for  {city.capitalize()},  {country_code.upper()}  [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
             "green",
             attrs=["bold"],
         )
     )
    # rest of the code

def print_day_time_forecast(data):
    """Print the day time forecast data."""
    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    # rest of the code

def print_night_time_forecast(data):
    """Print the night time forecast data."""
    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    # rest of the code

def print_forecast_for_next_5_days(data):
    """Print the forecast for next 5 days data."""
    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    # rest of the code

def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime)  -> str:
    """Format the weather data to CLI response."""
    print_current_weather(data, city, country_code)
    print_day_time_forecast(data)
    print_night_time_forecast(data)
    print_forecast_for_next_5_days(data)

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
