from dataclasses import dataclass, field
from typing import List

@dataclass
class Weather:
    main: str

@dataclass
class Wind:
    speed: float

@dataclass
class CurrentWeather:
    temp: float
    feels_like: float
    humidity: int
    temp_min: float
    temp_max: float

@dataclass
class Forecast:
    dt_txt: str
    main: dict
    weather: List[Weather]

@dataclass
class CityWeather:
    city: str
    current_weather: CurrentWeather
    forecast: List[Forecast]

def parse_json_for_city(response, city):
    """Prints the weather with the given command-line option."""
    if option == '-f' or option == '-F':
        print(f"5-day Forecast for {city}")
        day = ""
        for forecast in response['list']:
            if day == forecast['dt_txt'][:10]:
                print(f"Time: {forecast['dt_txt'][11:16]} Temperature: {response['main']['temp']:.1f}{met[option][0]} Weather: {forecast['weather'][0]['main']}")
            else:
                day = forecast['dt_txt'][:10]
                print("-------------------------------------------------------")
                print(f"Date: {day}")
                print(f"Time: {forecast['dt_txt'][11:16]} Temperature: {response['main']['temp']:.1f}{met[option][0]} Weather: {forecast['weather'][0]['main']}")
    else:
        print("-------------------------------------------------------")
        print(f"Current Weather for {city}")
        print(f"Temperature: {response['main']['temp']:.1f}{met[option][0]}")
        print(f"Wind Speed: {response['wind']['speed']:.1f}{met[option][1]}")
        print(f"Weather: {response['weather'][0]['main']}")
        print(f"Feels Like: {response['main']['feels_like']:.1f}{met[option][0]}")
        print(f"Humidity: {response['main']['humidity']}%")
        print(f"Minimum Temperature: {response['main']['temp_min']:.1f}{met[option][0]}")
        print(f"Maximum Temperature: {response['main']['temp_max']:.1f}{met[option][0]}")
        print("-------------------------------------------------------")


def run(response, city, option_flag):
    """Prints the weather with the given command-line option. Public entry point of this unit."""
    global option
    option = option_flag
    parse_json_for_city(response, city)
