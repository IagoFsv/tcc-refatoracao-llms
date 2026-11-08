from dataclasses import dataclass, field
from typing import List

@dataclass
class Weather:
    name: str
    weather: List[dict] = field(default_factory=list)

@dataclass
class WeatherDescription:
    description: str

@dataclass
class CityWeather:
    city: str
    description: WeatherDescription

def print_weather(weather: CityWeather):
    if weather is not None:
        print(f"The weather in {weather.city} is {weather.description.description}")
    else:
        print("Error: Could not get weather")


def executar(weather: Weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    city_weather = CityWeather(
        city=weather.name,
        description=WeatherDescription(
            description=weather.weather[0]["description"]
        )
    )
    print_weather(city_weather)
