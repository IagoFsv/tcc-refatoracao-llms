"""Current weather of a city, printed on the terminal.

Public entry point: run(weather). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def print_weather(weather):
    if weather is not None:
        weather_details = weather.get("weather")
        if weather_details and weather_details[0]:
            description = weather_details[0].get("description")
            if description:
                print(f"The weather in {weather['name']} is {description}")
            else:
                print("Error: Weather description not found")
        else:
            print("Error: Weather details not found")
    else:
        print("Error: Could not get weather")


def run(weather):
    """Prints the weather received from the API. Public entry point of this unit."""
    print_weather(weather)
