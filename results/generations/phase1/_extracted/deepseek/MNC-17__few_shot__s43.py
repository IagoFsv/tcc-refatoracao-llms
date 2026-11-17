"""Current weather of a city, printed on the terminal.

Public entry point: run(weather). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

from typing import Optional

class Weather:
    def __init__(self, weather_data):
        self.data = weather_data

    @property
    def name(self):
        return self.data["name"]

    @property
    def description(self):
        return self.data["weather"][0]["description"]


def print_weather(weather: Optional[Weather]):
    if weather is not None:
        print(f"The weather in {weather.name} is {weather.description}")
    else:
        print("Error: Could not get weather")


def run(weather):
    """Prints the weather received from the API. Public entry point of this unit."""
    weather = Weather(weather)
    print_weather(weather)
