from termcolor import colored
from datetime import datetime

def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")

def format_weather_data(data):
    """Format the weather data."""
    return {
        'current': {
            'Time': data.get('current', {}).get('Time', 'N/A'),
            'Temp': data.get('current', {}).get('Temp', 'N/A'),
            'Phrase': data.get('current', {}).get('Phrase', 'N/A'),
            'Realfeel sun': data.get('current', {}).get('Realfeel sun', 'N/A'),
            'Realfeel shade': data.get('current', {}).get('Realfeel shade', 'N/A'),
            'Max uv index': data.get('current', {}).get('Max uv index', 'N/A'),
            'Wind': data.get('current', {}).get('Wind', ' N/A')[1:],
            'Wind gusts': data.get('current', {}).get('Wind gusts', 'N/A'),
            'Cloud cover': data.get('current', {}).get('Cloud cover', 'N/A'),
            'Dew point': data.get('current', {}).get('Dew point', 'N/A'),
            'Humidity': data.get('current', {}).get('Humidity', 'N/A'),
            'Indoor humidity': data.get('current', {}).get('Indoor humidity', 'N/A'),
            'Visibility': data.get('current', {}).get('Visibility', 'N/A'),
            'Pressure': data.get('current', {}).get('Pressure', 'N/A'),
            'Cloud ceiling': data.get('current', {}).get('Cloud ceiling', 'N/A')
        },
        'day': {
            'Temp': data.get('day', {}).get('Temp', 'N/A'),
            'Phrase': data.get('day', {}).get('Phrase', 'N/A'),
            'Max UV Index': data.get('day', {}).get('Max UV Index', 'N/A'),
            'Wind': data.get('day', {}).get('Wind', 'N/A'),
            'Wind Gusts': data.get('day', {}).get('Wind Gusts', 'N/A'),
            'Cloud Cover': data.get('day', {}).get('Cloud Cover', 'N/A'),
            'Rain': data.get('day', {}).get('Rain', 'N/A'),
            'Probability of Thunderstorms': data.get('day', {}).get('Probability of Thunderstorms', 'N/A')
        },
        'night': {
            'Temp': data.get('night', {}).get('Temp', 'N/A'),
            'Phrase': data.get('night', {}).get('Phrase', 'N/A'),
            'Max UV Index': data.get('night', {}).get('Max UV Index', 'N/A'),
            'Wind': data.get('night', {}).get('Wind', 'N/A'),
            'Wind Gusts': data.get('night', {}).get('Wind Gusts', 'N/A'),
            'Cloud Cover': data.get('night', {}).get('Cloud Cover', 'N/A'),
            'Rain': data.get('night', {}).get('Rain', 'N/A'),
            'Probability of Thunderstorms': data.get('night', {}).get('Probability of Thunderstorms', 'N/A')
        },
        'forecast': data.get("forecast", [])
    }

def print_weather(data, city: str, country_code: str, start_time: datetime):
    """Print the weather data to CLI."""
    print(
        colored(
            f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print(colored(f" - {data['current']['Time']} | Temp: {data['current']['Temp']} | Feels: {data['current']['Phrase']} | AQI (?)", "red"))
    print(colored(f" - RealFeel Sun: {data['current']['Realfeel sun']} | RealFeel Shade: {data['current']['Realfeel shade']} | UV Index: {data['current']['Max uv index']}", "blue"))
    print(colored(f" - Wind: {data['current']['Wind']} | Gusts: {data['current']['Wind gusts']} | Cloud Cover: {data['current']['Cloud cover']}", "green"))
    print(colored(f" - Dew Point: {data['current']['Dew point']} | Humidity: {data['current']['Humidity']} | Indoor Humidity: {data['current']['Indoor humidity']}", "cyan"))
    print(colored(f" - Visibility: {data['current']['Visibility']} | Pressure: {data['current']['Pressure']} | Ceiling: {data['current']['Cloud ceiling']}", "yellow"))

    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    print(colored(f" - Temp: {data['day']['Temp']} | Feels: {data['day']['Phrase']} | AQI (?)", "yellow"))
    print(colored(f" - UV Index: {data['day']['Max UV Index']} | Wind: {data['day']['Wind']} | Gusts: {data['day']['Wind Gusts']}", "green"))
    print(colored(f" - Cloud Cover: {data['day']['Cloud Cover']} | Rain: {data['day']['Rain']} | Thunder: {data['day']['Probability of Thunderstorms']}", "blue"))

    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    print(colored(f" - Temp: {data['night']['Temp']} | Feels: {data['night']['Phrase']} | AQI (?)", "yellow"))
    print(colored(f" - UV Index: {data['night']['Max UV Index']} | Wind: {data['night']['Wind']} | Gusts: {data['night']['Wind Gusts']}", "green"))
    print(colored(f" - Cloud Cover: {data['night']['Cloud Cover']} | Rain: {data['night']['Rain']} | Thunder: {data['night']['Probability of Thunderstorms']}", "blue"))

    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    for i in range(5):
        print(colored(f" -> {data['forecast'][i]['Date']} | {data['forecast'][i]['Temp']['max']} >>>>> {data['forecast'][i]['Temp']['min']}", "magenta"))
        print(colored(" " * 3 + f"- Rain: {data['forecast'][i]['Rain']} | Hours of Rain: {data['forecast'][i]['Hours of Precipitation']} | Cloud Cover: {data['forecast'][i]['Cloud Cover']}", "green"))
        print(colored(" " * 3 + f"- Wind: {data['forecast'][i]['Wind']} | Gusts: {data['forecast'][i]['Wind Gusts']} | Thunder: {data['forecast'][i]['Probability of Thunderstorms']}", "yellow"))

    print(
        colored(
            "\n " + "-" * 17 + f"{colored(f'Powered by AccuWeather ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}" + f"{colored('-'* 17, 'red')}",
            "green",
        )
    )

def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    data = format_weather_data(dados)
    return print_weather(data, cidade, codigo_pais, datetime.now())
