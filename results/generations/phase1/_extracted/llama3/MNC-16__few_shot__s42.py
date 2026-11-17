"""Weather forecast of a city, printed on the terminal.

Public entry point: run(response, city, option_flag). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

option = '-c'

def WeatherForecast(city, response, option_flag):
    if option_flag in ['-f', '-F', '-c', '-C']:
        print(f"5-day Forecast for {city}")
        day = ""
        for weather_data in response['list']:
            if day == weather_data['dt_txt'][:10]:
                print(f"Time: {weather_data['dt_txt'][11:16]} Temperature: {'%.1f' % weather_data['main']['temp']} {met[option_flag][0]} Weather: {weather_data['weather'][0]['main']}")
            else:
                day = weather_data['dt_txt'][:10]
                print("-------------------------------------------------------")
                print(f"Date: {day}")
                print(f"Time: {weather_data['dt_txt'][11:16]} Temperature: {'%.1f' % weather_data['main']['temp']} {met[option_flag][0]} Weather: {weather_data['weather'][0]['main']}")
    else:
        print("-------------------------------------------------------")
        print(f"Current Weather for {city}")
        #convert to centrigrade and set precision 1
        print(f"Temperature: {'%.1f' % response['main']['temp']} {met[option_flag][0]}")
        print(f"Wind Speed: {'%.1f' % response['wind']['speed']} {met[option_flag][1]}")
        print(f"Weather: {response['weather'][0]['main']}")
        #print other conditions including feels like,humidity, temp_min, temp_max
        print(f"Feels Like: {'%.1f' % response['main']['feels_like']} {met[option_flag][0]}")
        print(f"Humidity: {response['main']['humidity']} %")
        print(f"Minimum Temperature: {'%.1f' % response['main']['temp_min']} {met[option_flag][0]}")
        print(f"Maximum Temperature: {'%.1f' % response['main']['temp_max']} {met[option_flag][0]}")
        print("-------------------------------------------------------")


def run(response, city, option_flag):
    """Prints the weather with the given command-line option. Public entry point of this unit."""
    global option
    option = option_flag
    WeatherForecast(city, response, option_flag)
