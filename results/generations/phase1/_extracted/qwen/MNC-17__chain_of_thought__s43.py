"""Current weather of a city, printed on the terminal.

Public entry point: run(weather). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def print_weather(weather):
    if weather is None:
        print("Error: Could not get weather")
    else:
        city_name = weather.get("name")
        weather_description = weather.get("weather", [{}])[0].get("description")
        
        if city_name and weather_description:
            print(f"The weather in {city_name} is {weather_description}")
        else:
            print("Error: Invalid weather data")


def run(weather):
    """Prints the weather received from the API. Public entry point of this unit."""
    print_weather(weather)
