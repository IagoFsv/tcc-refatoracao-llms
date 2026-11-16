from termcolor import colored
from datetime import datetime

def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a,  %d-%b-%y")

def get_weather_data(data, category, color):
    """Get weather data for a specific category."""
    return colored(
            f"  - {data.get('current', {}).get('Time', 'N/A')} | Temp: {data.get('current', {}).get('Temp', 'N/A')} | Feels: {data.get('current', {}).get('Phrase', 'N/A')} | AQI (?)",
             color,
         )

def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime)  -> str:
    """Format the weather data to CLI response."""
    print(
        colored(
            f"[*] Current Weather for  {city.capitalize()},  {country_code.upper()}  [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
         )
    )
    print(get_weather_data(data, 'current', 'red'))
    print(get_weather_data(data, 'real feel sun', 'blue'))
    print(get_weather_data(data, 'real feel shade', 'blue'))
    print(get_weather_data(data, 'uv index', 'green'))
    print(get_weather_data(data, 'wind', 'green'))
    print(get_weather_data(data, 'gusts', 'green'))
    print(get_weather_data(data, 'cloud cover', 'blue'))
    print(get_weather_data(data, 'dew point', 'cyan'))
    print(get_weather_data(data, 'humidity', 'cyan'))
    print(get_weather_data(data, 'indoor humidity', 'cyan'))
    print(get_weather_data(data, 'visibility', 'yellow'))
    print(get_weather_data(data, 'pressure', 'yellow'))
    print(get_weather_data(data, 'ceiling', 'yellow'))

    # Rest of the code remains the same

def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    return fmt_cli_resp(dados, cidade, codigo_pais, datetime.now())
