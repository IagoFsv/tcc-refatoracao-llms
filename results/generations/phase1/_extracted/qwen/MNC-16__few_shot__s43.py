"""Weather forecast of a city, printed on the terminal.

Public entry point: run(response, city, option_flag). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

option = '-c'

def parseJSONforCITY(response, CITY):
    '''
    print only for key = main, key = wind speed and key = weather[main] in a pretty format
    '''

    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}

    if option == '-f' or option == '-F':
        print("5-day Forecast for " + CITY)
        """check for date field
           if the day is same, print the content in the same line
           if the day is different, print the content in the next line
        """
        day = ""
        for forecast in response['list']:
            forecast_date = forecast['dt_txt'][0:10]
            forecast_time = forecast['dt_txt'][11:16]
            forecast_temp = forecast['main']['temp']
            forecast_weather = forecast['weather'][0]['main']

            if day == forecast_date:
                print("Time: " + forecast_time + " Temperature: " + str('%.1f' % forecast_temp) + met[option][0] + " Weather: " + forecast_weather)
            else:
                day = forecast_date
                print("-------------------------------------------------------")
                print("Date: " + day)
                print("Time: " + forecast_time + " Temperature: " + str('%.1f' % forecast_temp) + met[option][0] + " Weather: " + forecast_weather)             

    else:
        print("-------------------------------------------------------")
        print("Current Weather for " + CITY)
        #convert to centrigrade and set precision 1
        current_temp = response['main']['temp']
        wind_speed = response['wind']['speed']
        current_weather = response['weather'][0]['main']
        feels_like = response['main']['feels_like']
        humidity = response['main']['humidity']
        temp_min = response['main']['temp_min']
        temp_max = response['main']['temp_max']

        print("Temperature: " + str('%.1f' % current_temp) + met[option][0])
        print("Wind Speed: " + str('%.1f' % wind_speed) + met[option][1])
        print("Weather: " + current_weather)
        #print other conditions including feels like,humidity, temp_min, temp_max
        print("Feels Like: " + str('%.1f' % feels_like) + met[option][0])
        print("Humidity: " + str(humidity) + "%")
        print("Minimum Temperature: " + str('%.1f' %  temp_min) + met[option][0])
        print("Maximum Temperature: " + str('%.1f' %  temp_max) + met[option][0])
        print("-------------------------------------------------------")


def run(response, city, option_flag):
    """Prints the weather with the given command-line option. Public entry point of this unit."""
    global option
    option = option_flag
    parseJSONforCITY(response, city)
