"""Current weather of a city, printed on the terminal.

Public entry point: run(weather). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def print_weather(weather):
    if weather != None:
        city_name = weather["name"]
        weather_description = weather["weather"][0]["description"]
        print("The weather in " + city_name + " is " + weather_description)
    else:
        print("Error: Could not get weather")


def run(weather):
    """Prints the weather received from the API. Public entry point of this unit."""
    print_weather(weather)
