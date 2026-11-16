from termcolor import colored
from datetime import datetime

def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")

def print_weather_section(data, section, title_color, text_color):
    """Print a section of the weather data."""
    print(colored(f"\n[*] {title}", title_color, attrs=["bold"]))
    for key, value in data[section].items():
        print(colored(f" - {key.capitalize()}: {value if value else 'N/A'}", text_color))

def print_forecast_section(forecast, section, title_color, text_color):
    """Print a section of the forecast data."""
    print(colored(f"\n[*] {section} Forecast", title_color, attrs=["bold"]))
    for i in range(5):
        print(colored(f" -> {forecast[i+1].get('Date', 'N/A')} | {forecast[i+1].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[i+1].get('Temp', {}).get('min', 'N/A')}", title_color))
        print(colored(f" " * 3 + f"- Rain: {forecast[i+1].get('Rain', 'N/A')} | Hours of Rain: {forecast[i+1].get('Hours of Precipitation', 'N/A')} | Cloud Cover: {forecast[i+1].get('Cloud Cover', 'N/A')}", text_color))
        print(colored(f" " * 3 + f"- Wind: {forecast[i+1].get('Wind', ' N/A')[1:]} | Gusts: {forecast[i+1].get('Wind Gusts', 'N/A')} | Thunder: {forecast[i+1].get('Probability of Thunderstorms', 'N/A')}", text_color))

def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    print(colored(f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}", "green", attrs=["bold"]))
    print_weather_section(data, "current", "red", "red")
    print_weather_section(data, "day", "red", "green")
    print_weather_section(data, "night", "red", "blue")

    print_forecast_section(data, "Forecast for next 5 days", "red", "magenta")

    print(colored(f"\n {colored(f'Powered by AccuWeather ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}{colored('-'* 17, 'red')}", "green"))

def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    return fmt_cli_resp(dados, cidade, codigo_pais, datetime.now())
