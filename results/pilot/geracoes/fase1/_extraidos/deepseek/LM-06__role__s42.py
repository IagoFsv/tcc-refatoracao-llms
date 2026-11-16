from termcolor import colored
from datetime import datetime

def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a,  %d-%b-%y")

def print_weather_data(data, city: str, country_code: str, start_time: datetime):
    """Format the weather data to CLI response."""
    print(f"[*] Current Weather for  {city.capitalize()},  {country_code.upper()} [{get_current_date()}]")
    print(f"  -  {data.get('current',  {}).get('Time',  'N/A')} | Temp:  {data.get('current',  {}).get('Temp',  'N/A')} | Feels:  {data.get('current',  {}).get('Phrase',  'N/A')} | AQI (?)")
    print(f"  - RealFeel Sun:  {data.get('current',  {}).get('Realfeel sun',  'N/A')} | RealFeel Shade:  {data.get('current',  {}).get('Realfeel shade',  'N/A')} | UV Index:  {data.get('current',  {}).get('Max uv index',  'N/A')}")
    print(f"  - Wind:  {data.get('current',  {}).get('Wind',  ' N/A')[1:]} | Gusts:  {data.get('current',  {}).get('Wind gusts',  'N/A')} | Cloud Cover:  {data.get('current',  {}).get('Cloud cover',  'N/A')}")
    print(f"  - Dew Point:  {data.get('current',  {}).get('Dew point',  'N/A')} | Humidity:  {data.get('current',  {}).get('Humidity',  'N/A')} | Indoor Humidity:  {data.get('current',  {}).get('Indoor humidity',  'N/A')}")
    print(f"  - Visibility:  {data.get('current',  {}).get('Visibility',  'N/A')} | Pressure:  {data.get('current',  {}).get('Pressure',  'N/A')} | Ceiling:  {data.get('current',  {}).get('Cloud ceiling',  'N/A')}")

    print("\n[*] DayTime Forecast")
    print(f"  - Temp:  {data.get('day',  {}).get('Temp',  'N/A')} | Feels:  {data.get('day',  {}).get('Phrase',  'N/A')} | AQI (?)")
    print(f"  - UV Index:  {data.get('day',  {}).get('Max UV Index',  'N/A')} | Wind:  {data.get('day',  {}).get('Wind',  'N/A')} | Gusts:  {data.get('day',  {}).get('Wind Gusts',  'N/A')}")
    print(f"  - Cloud Cover:  {data.get('day',  {}).get('Cloud Cover',  'N/A')} | Rain:  {data.get('day',  {}).get('Rain',  'N/A')} | Thunder:  {data.get('day',  {}).get('Probability of Thunderstorms',  'N/A')}")

    print("\n[*] NightTime Forecast")
    print(f"  - Temp:  {data.get('night',  {}).get('Temp',  'N/A')} | Feels:  {data.get('night',  {}).get('Phrase',  'N/A')} | AQI (?)")
    print(f"  - UV Index:  {data.get('night',  {}).get('Max UV Index',  'N/A')} | Wind:  {data.get('night',  {}).get('Wind',  'N/A')} | Gusts:  {data.get('night',  {}).get('Wind Gusts',  'N/A')}")
    print(f"  - Cloud Cover:  {data.get('night',  {}).get('Cloud Cover',  'N/A')} | Rain:  {data.get('night',  {}).get('Rain',  'N/A')} | Thunder:  {data.get('night',  {}).get('Probability of Thunderstorms',  'N/A')}")

    print("\n[*] Forecast for next 5 days")
    forecast = data.get("forecast",  [])
    for i in range(5):
        print(f"  -> {forecast[i+1].get('Date',  'N/A')} | {forecast[i+1].get('Temp',  {}).get('max',  'N/A')} >>>>> {forecast[i+1].get('Temp',  {}).get('min',  'N/A')}")
        print("  " * 3 + f"- Rain:  {forecast[i+1].get('Rain',  'N/A')} | Hours of Rain:  {forecast[i+1].get('Hours of Precipitation',  'N/A')} | Cloud Cover:  {forecast[i+1].get('Cloud Cover',  'N/A')}")
        print("  " * 3 + f"- Wind:  {forecast[i+1].get('Wind',  ' N/A')[1:]} | Gusts:  {forecast[i+1].get('Wind Gusts',  'N/A')} | Thunder:  {forecast[i+1].get('Probability of Thunderstorms',  'N/A')}")
    print(f"\n {'-'* 17}Powered by AccuWeather  ({round((datetime.now()  - start_time).total_seconds(), 2)}s){'-'* 17}")

def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    return print_weather_data(dados, cidade, codigo_pais, datetime.now())
