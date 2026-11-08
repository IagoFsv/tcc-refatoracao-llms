"""Resposta de linha de comando com o clima atual e a previsao.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a,  %d-%b-%y")


def format_weather_data(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    return (
        f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{get_current_date()}]\n"
        f"  - {data.get('current', {}).get('Time', 'N/A')} | Temp: {data.get('current', {}).get('Temp', 'N/A')} | Feels: {data.get('current', {}).get('Phrase', 'N/A')} | AQI  (?)\n"
        f"  - RealFeel Sun: {data.get('current', {}).get('Realfeel sun', 'N/A')} | RealFeel Shade: {data.get('current', {}).get('Realfeel shade', 'N/A')} | UV Index: {data.get('current', {}).get('Max uv index', 'N/A')}\n"
        f"  - Wind: {data.get('current', {}).get('Wind', ' N/A')[1:]} | Gusts: {data.get('current', {}).get('Wind gusts', 'N/A')} | Cloud Cover: {data.get('current', {}).get('Cloud cover', 'N/A')}\n"
        f"  - Dew Point: {data.get('current', {}).get('Dew point', 'N/A')} | Humidity: {data.get('current', {}).get('Humidity', 'N/A')} | Indoor Humidity: {data.get('current', {}).get('Indoor humidity', 'N/A')}\n"
        f"  - Visibility: {data.get('current', {}).get('Visibility', 'N/A')} | Pressure: {data.get('current', {}).get('Pressure', 'N/A')} | Ceiling: {data.get('current', {}).get('Cloud ceiling', 'N/A')}\n"
        f"\n[*] DayTime Forecast\n"
        f"  - Temp: {data.get('day', {}).get('Temp', 'N/A')} | Feels: {data.get('day', {}).get('Phrase', 'N/A')} | AQI  (?)\n"
        f"  - UV Index: {data.get('day', {}).get('Max UV Index', 'N/A')} | Wind: {data.get('day', {}).get('Wind', 'N/A')} | Gusts: {data.get('day', {}).get('Wind Gusts', 'N/A')}\n"
        f"  - Cloud Cover: {data.get('day', {}).get('Cloud Cover', 'N/A')} | Rain: {data.get('day', {}).get('Rain', 'N/A')} | Thunder: {data.get('day', {}).get('Probability of Thunderstorms', 'N/A')}\n"
        f"\n[*] NightTime Forecast\n"
        f"  - Temp: {data.get('night', {}).get('Temp', 'N/A')} | Feels: {data.get('night', {}).get('Phrase', 'N/A')} | AQI  (?)\n"
        f"  - UV Index: {data.get('night', {}).get('Max UV Index', 'N/A')} | Wind: {data.get('night', {}).get('Wind', 'N/A')} | Gusts: {data.get('night', {}).get('Wind Gusts', 'N/A')}\n"
        f"  - Cloud Cover: {data.get('night', {}).get('Cloud Cover', 'N/A')} | Rain: {data.get('night', {}).get('Rain', 'N/A')} | Thunder: {data.get('night', {}).get('Probability of Thunderstorms', 'N/A')}\n"
        f"\n[*] Forecast for next 5 days\n"
        f"  -> {forecast[i+1].get('Date', 'N/A')} | {forecast[i+1].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[i+1].get('Temp', {}).get('min', 'N/A')}\n"
        f"  - Rain: {forecast[i+1].get('Rain', 'N/A')} | Hours of Rain: {forecast[i+1].get('Hours of Precipitation', 'N/A')} | Cloud Cover: {forecast[i+1].get('Cloud Cover', 'N/A')}\n"
        f"  - Wind: {forecast[i+1].get('Wind', ' N/A')[1:]} | Gusts: {forecast[i+1].get('Wind Gusts', 'N/A')} | Thunder: {forecast[i+1].get('Probability of Thunderstorms', 'N/A')}\n"
        f"\n Powered by AccuWeather ({round((datetime.now() - start_time).total_seconds(), 2)}s)\n"
    )


def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    start_time = datetime.now()
    return format_weather_data(dados, cidade, codigo_pais, start_time)
