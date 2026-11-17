"""Current weather of a city, printed on the terminal.

Public entry point: run(weather). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def print_weather(weather):
    if weather != None:
        print("The weather in " + weather["name"] + " is " + weather["weather"][0]["description"])
    else:
        print("Error: Could not get weather")


def get_city_name(weather):
    return weather["name"]

def get_weather_description(weather):
    return weather["weather"][0]["description"]

def run(weather):
    """Prints the weather received from the API. Public entry point of this unit."""
    print_weather(weather)
