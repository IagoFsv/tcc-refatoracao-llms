"""Current weather of a city, printed on the terminal.

Public entry point: run(weather). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def get_weather_description(weather):
    if weather is not None and "weather" in weather and len(weather["weather"]) > 0:
        return weather["weather"][0]["description"]
    return None

def print_weather(weather):
    description = get_weather_description(weather)
    if description is not None:
        print("The weather in " + weather["name"] + " is " + description)
    else:
        print("Error: Could not get weather")


def run(weather):
    """Prints the weather received from the API. Public entry point of this unit."""
    print_weather(weather)
