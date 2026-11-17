"""Weather forecast of a city, printed on the terminal.

Public entry point: run(response, city, option_flag). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

option = '-c'

def parse_weather(response):
    return response['weather'][0]['main']

def parse_main(response):
    return response['main']

def parse_wind(response):
    return response['wind']

def parseJSONforCITY(response, CITY):
    '''
    print only for key = main, key = wind speed and key = weather[main] in a pretty format
    '''

    met = {'-f': ('°C', 'm/s'), '-F': ('°F', 'mph'), '-c': ('°C', 'm/s'), '-C': ('°F', 'mph')}

    if option == '-f' or option == '-F':
        print_forecast(response, CITY, met)
    else:
        print_current_weather(response, CITY, met)

def print_current_weather(response, CITY, met):
    print("-------------------------------------------------------")
    print("Current Weather for " + CITY)
    print_temperature(response, met[option][0])
    print_wind_speed(response, met[option][1])
    print("Weather: " + parse_weather(response))
    print_other_conditions(response, met[option][0])

def print_forecast(response, CITY, met):
    print("5-day Forecast for " + CITY)
    for weather in response['list']:
        print_weather_for_day(weather, met)

def print_weather_for_day(weather, met):
    day = weather['dt_txt'][0:10]
    print("-------------------------------------------------------")
    print("Date: " + day)
    print("Time: " + weather['dt_txt'][11:16])
    print_temperature(weather, met[0])
    print("Weather: " + parse_weather(weather))

def print_temperature(data, unit):
    print("Temperature: " + str('%.1f' % (parse_main(data)['temp'])) + unit)

def print_wind_speed(data, unit):
    print("Wind Speed: " + str('%.1f' % (parse_wind(data)['speed'])) + unit)

def print_other_conditions(data, unit):
    print("Feels Like: " + str('%.1f' % (parse_main(data)['feels_like'])) + unit)
    print("Humidity: " + str(parse_main(data)['humidity']) + "%")
    print("Minimum Temperature: " + str('%.1f' % (parse_main(data)['temp_min'])) + unit)
    print("Maximum Temperature: " + str('%.1f' % (parse_main(data)['temp_max'])) + unit)

def run(response, city, option_flag):
    """Prints the weather with the given command-line option. Public entry point of this unit."""
    global option
    option = option_flag
    parseJSONforCITY(response, city)
