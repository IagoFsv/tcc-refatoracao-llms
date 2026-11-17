"""Current weather of a city, printed on the terminal.

Public entry point: run(weather). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def print_weather(location, description):
    if location and description != None:
        print("The weather in " + location["name"] + " is " + description["description"])
    else:
        print("Error: Could not get weather")

def decompose_weather(weather):
    if weather:
        return weather["name"], weather["weather"][0]
    else:
        return None, None

def run(weather):
    """Prints the weather received from the API. Public entry point of this unit."""
    location, description = decompose_weather(weather)
    print_weather(location, description)
