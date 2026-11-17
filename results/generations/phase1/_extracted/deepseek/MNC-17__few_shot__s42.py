"""Current weather of a city, printed on the terminal.

Public entry point: run(weather). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

from typing import Optional

class Weather:
    def __init__(self, data: dict):
        self.data = data

    def get_name(self) -> Optional[str]:
        return self.data.get("name")

    def get_description(self) -> Optional[str]:
        return self.data.get("weather", [{}])[0].get("description")


def print_weather(weather: Weather):
    if weather is not None:
        print("The weather in " + weather.get_name() + " is " + weather.get_description())
    else:
        print("Error: Could not get weather")


def run(weather: dict):
    """Prints the weather received from the API. Public entry point of this unit."""
    weather = Weather(weather)
    print_weather(weather)
