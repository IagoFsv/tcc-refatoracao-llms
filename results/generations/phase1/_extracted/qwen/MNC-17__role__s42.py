"""Current weather of a city, printed on the terminal.

Public entry point: run(weather). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def print_weather(weather):
    if weather is not None:
        weather_data = weather.get("weather")
        if weather_data and len(weather_data) > 0:
            description = weather_data[0].get("description")
            city_name = weather.get("name")
            if city_name and description:
                print(f"The weather in {city_name} is {description}")
            else:
                print("Error: Missing data in weather response")
        else:
            print("Error: Invalid weather data structure")
    else:
        print("Error: Could not get weather")


def run(weather):
    """Prints the weather received from the API. Public entry point of this unit."""
    print_weather(weather)
