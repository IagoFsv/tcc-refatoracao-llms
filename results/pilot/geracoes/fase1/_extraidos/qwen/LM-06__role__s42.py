from termcolor import colored
from datetime import datetime

def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")

def print_weather_section(data, section, start_time):
    """Print a section of weather data."""
    print(colored(f"\n[*] {section} Forecast", "red", attrs=["bold"]))
    for key, value in data.items():
        print(
            colored(
                f" - {key.capitalize()}: {value.get('Temp', 'N/A')} | Feels: {value.get('Phrase', 'N/A')} | AQI (?)",
                "yellow" if "Day" in section else "green" if "Night" in section else "blue",
            )
        )
        print(
            colored(
                f" - UV Index: {value.get('Max UV Index', 'N/A')} | Wind: {value.get('Wind', 'N/A')} | Gusts: {value.get('Wind Gusts', 'N/A')}",
                "green" if "Day" in section else "yellow" if "Night" in section else "blue",
            )
        )
        print(
            colored(
                f" - Cloud Cover: {value.get('Cloud Cover', 'N/A')} | Rain: {value.get('Rain', 'N/A')} | Thunder: {value.get('Probability of Thunderstorms', 'N/A')}",
                "blue" if "Day" in section else "green" if "Night" in section else "yellow",
            )
        )

def print_forecast_section(forecast):
    """Print the forecast for the next 5 days."""
    for i in range(5):
        print(
            colored(
                f" -> {forecast[i+1].get('Date', 'N/A')} | {forecast[i+1].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[i+1].get('Temp', {}).get('min', 'N/A')}",
                "magenta",
            )
        )
        print(
            colored(
                " " * 3
                + f"- Rain: {forecast[i+1].get('Rain', 'N/A')} | Hours of Rain: {forecast[i+1].get('Hours of Precipitation', 'N/A')} | Cloud Cover: {forecast[i+1].get('Cloud Cover', 'N/A')}",
                "green",
            )
        )
        print(
            colored(
                " " * 3
                + f"- Wind: {forecast[i+1].get('Wind', ' N/A')[1:]} | Gusts: {forecast[i+1].get('Wind Gusts', 'N/A')} | Thunder: {forecast[i+1].get('Probability of Thunderstorms', 'N/A')}",
                "yellow",
            )
        )

def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
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
    print(
        colored(
            f" - RealFeel Sun: {data.get('current', {}).get('Realfeel sun', 'N/A')} | RealFeel Shade: {data.get('current', {}).get('Realfeel shade', 'N/A')} | UV Index: {data.get('current', {}).get('Max uv index', 'N/A')}",
            "blue",
        )
    )
    print(
        colored(
            f" - Wind: {data.get('current', {}).get('Wind', ' N/A')[1:]} | Gusts: {data.get('current', {}).get('Wind gusts', 'N/A')} | Cloud Cover: {data.get('current', {}).get('Cloud cover', 'N/A')}",
            "green",
        )
    )
    print(
        colored(
            f" - Dew Point: {data.get('current', {}).get('Dew point', 'N/A')} | Humidity: {data.get('current', {}).get('Humidity', 'N/A')} | Indoor Humidity: {data.get('current', {}).get('Indoor humidity', 'N/A')}",
            "cyan",
        )
    )
    print(
        colored(
            f" - Visibility: {data.get('current', {}).get('Visibility', 'N/A')} | Pressure: {data.get('current', {}).get('Pressure', 'N/A')} | Ceiling: {data.get('current', {}).get('Cloud ceiling', 'N/A')}",
            "yellow",
        )
    )

    print_weather_section(data.get('day', {}), "DayTime", start_time)
    print_weather_section(data.get('night', {}), "NightTime", start_time)
    print_forecast_section(data.get("forecast", []))

def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    return fmt_cli_resp(dados, cidade, codigo_pais, datetime.now())
