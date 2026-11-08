from termcolor import colored
from datetime import datetime

def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a,  %d-%b-%y")

def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime)  -> str:
    """Format the weather data to CLI response."""
    print_data(data, city, country_code, start_time)

def print_data(data, city: str, country_code: str, start_time: datetime):
    """Print the formatted data."""
    print_current_weather(data, city, country_code)
    print_forecast(data, "DayTime")
    print_forecast(data, "NightTime")
    print_forecast_next_5_days(data)
    print_powered_by(start_time)

def print_current_weather(data, city: str, country_code: str):
    """Print current weather data."""
    print(colored(f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}", "green", attrs=["bold"]))
    print(colored(f"  - {data.get('current',  {}).get('Time',  'N/A')} | Temp: {data.get('current',  {}).get('Temp',  'N/A')} | Feels: {data.get('current',  {}).get('Phrase',  'N/A')} | AQI  (?)", "red"))
    print(colored(f"  - RealFeel Sun: {data.get('current',  {}).get('Realfeel sun',  'N/A')} | RealFeel Shade: {data.get('current',  {}).get('Realfeel shade',  'N/A')} | UV Index: {data.get('current',  {}).get('Max uv index',  'N/A')}", "blue"))
    print(colored(f"  - Wind: {data.get('current',  {}).get('Wind',  ' N/A')[1:]} | Gusts: {data.get('current',  {}).get('Wind gusts',  'N/A')} | Cloud Cover: {data.get('current',  {}).get('Cloud cover',  'N/A')}", "green"))
    print(colored(f"  - Dew Point: {data.get('current',  {}).get('Dew point',  'N/A')} | Humidity: {data.get('current',  {}).get('Humidity',  'N/A')} | Indoor Humidity: {data.get('current',  {}).get('Indoor humidity',  'N/A')}", "cyan"))
    print(colored(f"  - Visibility: {data.get('current',  {}).get('Visibility',  'N/A')} | Pressure: {data.get('current',  {}).get('Pressure',  'N/A')} | Ceiling: {data.get('current',  {}).get('Cloud ceiling',  'N/A')}", "yellow"))

def print_forecast(data, time_of_day: str):
    """Print forecast data."""
    print(colored(f"\n[*] {time_of_day} Forecast", "red", attrs=["bold"]))
    print(colored(f"  - Temp: {data.get(time_of_day,  {}).get('Temp',  'N/A')} | Feels: {data.get(time_of_day,  {}).get('Phrase',  'N/A')} | AQI  (?)", "yellow"))
    print(colored(f"  - UV Index: {data.get(time_of_day,  {}).get('Max UV Index',  'N/A')} | Wind: {data.get(time_of_day,  {}).get('Wind',  'N/A')} | Gusts: {data.get(time_of_day,  {}).get('Wind Gusts',  'N/A')}", "green"))
    print(colored(f"  - Cloud Cover: {data.get(time_of_day,  {}).get('Cloud Cover',  'N/A')} | Rain: {data.get(time_of_day,  {}).get('Rain',  'N/A')} | Thunder: {data.get(time_of_day,  {}).get('Probability of Thunderstorms',  'N/A')}", "blue"))

def print_forecast_next_5_days(data):
    """Print forecast data for next 5 days."""
    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print(colored(f"  -> {forecast[i+1].get('Date',  'N/A')} | {forecast[i+1].get('Temp',  {}).get('max',  'N/A')} >>>>> {forecast[i+1].get('Temp',  {}).get('min',  'N/A')}", "magenta"))
        print(colored(f"  " * 3 + f"- Rain: {forecast[i+1].get('Rain',  'N/A')} | Hours of Rain: {forecast[i+1].get('Hours of Precipitation',  'N/A')} | Cloud Cover: {forecast[i+1].get('Cloud Cover',  'N/A')}", "green"))
        print(colored(f"  " * 3 + f"- Wind: {forecast[i+1].get('Wind',  ' N/A')[1:]} | Gusts: {forecast[i+1].get('Wind Gusts',  'N/A')} | Thunder: {forecast[i+1].get('Probability of Thunderstorms',  'N/A')}", "yellow"))

def print_powered_by(start_time: datetime):
    """Print powered by message."""
    print(colored(f"\n " + "-" * 17 + f"{colored(f'Powered by AccuWeather  ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}" + f"{colored('-' * 17, 'red')}", "green"))

def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    return fmt_cli_resp(dados, cidade, codigo_pais, datetime.now())
