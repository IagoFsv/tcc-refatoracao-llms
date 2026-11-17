"""Current weather of a city, printed on the terminal.

Public entry point: run(weather). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

def get_city_name(weather):
    """Helper function to get the city name from the weather dictionary."""
    return weather.get("name", "Unknown")

def get_weather_description(weather):
    """Helper function to get the weather description from the weather dictionary."""
    if weather and "weather" in weather and len(weather["weather"]) > 0:
        return weather["weather"][0]["description"]
    return "Unknown"

def print_weather(weather):
    """Helper function to print the weather."""
    city_name = get_city_name(weather)
    weather_description = get_weather_description(weather)
    if weather is None:
        print("Error: Could not get weather")
    else:
        print("The weather in " + city_name + " is " + weather_description)

def run(weather):
    """Prints the weather received from the API. Public entry point of this unit."""
    print_weather(weather)
