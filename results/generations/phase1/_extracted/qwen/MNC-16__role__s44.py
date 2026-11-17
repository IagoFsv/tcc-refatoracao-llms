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

    if option in ('-f', '-F'):
        print("5-day Forecast for " + CITY)
        """check for date field
           if the day is same, print the content in the same line
           if the day is different, print the content in the next line
        """
        day = ""
        for forecast in response['list']:
            date = forecast['dt_txt'][0:10]
            if day == date:
                print("Time: " + forecast['dt_txt'][11:16] + " Temperature: " + str('%.1f' % (forecast['main']['temp'])) + met[option][0] + " Weather: " + forecast['weather'][0]['main'])
            else:
                day = date
                print("-------------------------------------------------------")
                print("Date: " + day)
                print("Time: " + forecast['dt_txt'][11:16] + " Temperature: " + str('%.1f' % (forecast['main']['temp'])) + met[option][0] + " Weather: " + forecast['weather'][0]['main'])             
    else:
        print("-------------------------------------------------------")
        print("Current Weather for " + CITY)
        #convert to centrigrade and set precision 1
        weather_data = response['main']
        wind_data = response['wind']
        weather_conditions = response['weather'][0]
        print("Temperature: " + str('%.1f' % (weather_data['temp'])) + met[option][0])
        print("Wind Speed: " + str('%.1f' % (wind_data['speed'])) + met[option][1])
        print("Weather: " + weather_conditions['main'])
        #print other conditions including feels like,humidity, temp_min, temp_max
        print("Feels Like: " + str('%.1f' % (weather_data['feels_like'])) + met[option][0])
        print("Humidity: " + str(weather_data['humidity']) + "%")
        print("Minimum Temperature: " + str('%.1f' %  (weather_data['temp_min'])) + met[option][0])
        print("Maximum Temperature: " + str('%.1f' %  (weather_data['temp_max'])) + met[option][0])
        print("-------------------------------------------------------")


def run(response, city, option_flag):
    """Prints the weather with the given command-line option. Public entry point of this unit."""
    global option
    option = option_flag
    parseJSONforCITY(response, city)
