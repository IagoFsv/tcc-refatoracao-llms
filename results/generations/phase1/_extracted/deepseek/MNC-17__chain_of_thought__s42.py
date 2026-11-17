"""Current weather of a city, printed on the terminal.

Public entry point: run(weather). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def extract_data(data, keys):
    """Extracts data from a nested dictionary using a list of keys."""
    for key in keys:
        try:
            data = data[key]
        except KeyError:
            return None
    return data

def print_weather(weather):
    if weather is not None:
        description = extract_data(weather, ["weather", 0, "description"])
        if description is not None:
            print("The weather in " + weather["name"] + " is " + description)
        else:
            print("Error: Could not get weather description")
    else:
        print("Error: Could not get weather")


def run(weather):
    """Prints the weather received from the API. Public entry point of this unit."""
    print_weather(weather)
