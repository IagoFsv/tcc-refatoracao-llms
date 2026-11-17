"""Weather forecast of a city, printed on the terminal.

Public entry point: run(response, city, option_flag). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

option = '-c'

def WeatherCondition(weather):
    return {
        'temp': f"{weather['main']['temp']:.1f}°{met[option][0]}",
        'wind_speed': f"{weather['wind']['speed']:.1f} {met[option][1]}",
        'main': weather['weather'][0]['main']
    }

def CityWeather(city, response):
    if option in ['-f', '-F']:
        print("5-day Forecast for " + city)
        for forecast in response['list']:
            print(f"Time: {forecast['dt_txt'][11:16]} {WeatherCondition(forecast['main'])}")
    else:
        print("-------------------------------------------------------")
        print(f"Current Weather for {city}")
        print(f"Temperature: {WeatherCondition(response['main'])}")
        print(f"Wind Speed: {WeatherCondition(response['wind'])}")
        print(f"Weather: {WeatherCondition(response['weather'][0])}")
        print("-------------------------------------------------------")

def run(response, city, option_flag):
    """Prints the weather with the given command-line option. Public entry point of this unit."""
    global option
    option = option_flag
    CityWeather(city, response)
