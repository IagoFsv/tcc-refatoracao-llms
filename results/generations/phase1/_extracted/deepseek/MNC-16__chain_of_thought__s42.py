"""Weather forecast of a city, printed on the terminal.

Public entry point: run(response, city, option_flag). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

option = '-c'

def parse_json_for_city(response, city):
    '''
    print only for key = main, key = wind speed and key = weather[main] in a pretty format
    '''
    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}

    if option in ['-f', '-F']:
        print_forecast(response, city, met)
    else:
        print_current_weather(response, city, met)


def print_forecast(response, city, met):
    print("5-day Forecast for " + city)
    print_forecast_helper(response, met)


def print_current_weather(response, city, met):
    print("-------------------------------------------------------")
    print("Current Weather for " + city)
    print_current_weather_helper(response, met)


def print_forecast_helper(response, met):
    day = ""
    for i in range(0, len(response['list'])):
        if day == response['list'][i]['dt_txt'][0:10]:
            print_forecast_line(response, i, met)
        else:
            day = response['list'][i]['dt_txt'][0:10]
            print_forecast_header(day)
            print_forecast_line(response, i, met)


def print_current_weather_helper(response, met):
    print_current_weather_line('Temperature', response['main']['temp'], met[option][0])
    print_current_weather_line('Wind Speed', response['wind']['speed'], met[option][1])
    print_current_weather_line('Weather', response['weather'][0]['main'], '')
    print_current_weather_line('Feels Like', response['main']['feels_like'], met[option][0])
    print_current_weather_line('Humidity', response['main']['humidity'], '%')
    print_current_weather_line('Minimum Temperature', response['main']['temp_min'], met[option][0])
    print_current_weather_line('Maximum Temperature', response['main']['temp_max'], met[option][0])
    print("-------------------------------------------------------")


def print_forecast_line(response, i, met):
    print("Time: " + response['list'][i]['dt_txt'][11:16] + " Temperature: " +
          str('%.1f' % (response['list'][i]['main']['temp'])) + met[option][0] +
          " Weather: " + response['list'][i]['weather'][0]['main'])


def print_forecast_header(day):
    print("-------------------------------------------------------")
    print("Date: " + day)


def print_current_weather_line(key, value, unit):
    print(key + ": " + str('%.1f' % value) + unit)


def run(response, city, option_flag):
    """Prints the weather with the given command-line option. Public entry point of this unit."""
    global option
    option = option_flag
    parse_json_for_city(response, city)
