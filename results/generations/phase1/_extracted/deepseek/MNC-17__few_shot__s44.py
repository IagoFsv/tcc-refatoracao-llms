from dataclasses import dataclass, field
from typing import List

@dataclass
class Weather:
    name: str
    weather: List[dict] = field(default_factory=list)

def print_weather(weather):
    if weather is not None:
        print(f"The weather in {weather.name} is {weather.weather[0]['description']}")
    else:
        print("Error: Could not get weather")

def run(weather):
    """Prints the weather received from the API. Public entry point of this unit."""
    weather = Weather(name=weather["name"], weather=weather["weather"])
    print_weather(weather)
