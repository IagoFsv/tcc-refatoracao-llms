"""Current weather of a city, printed on the terminal.

Public entry point: run(weather). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

from dataclasses import dataclass

@dataclass
class Weather:
    name: str
    weather: list[dict]

def print_weather(weather: Weather):
    if weather is not None:
        print(f"The weather in {weather.name} is {weather.weather[0]['description']}")
    else:
        print("Error: Could not get weather")


def run(weather: dict):
    """Prints the weather received from the API. Public entry point of this unit."""
    weather_data = Weather(**weather)
    print_weather(weather_data)
