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
        for i in range(0, len(response['list'])):
            current_day = response['list'][i]['dt_txt'][0:10]
            current_time = response['list'][i]['dt_txt'][11:16]
            current_temp = response['list'][i]['main']['temp']
            current_weather = response['list'][i]['weather'][0]['main']
            
            if day == current_day:
                print("Time: " + current_time + " Temperature: " + str('%.1f' % current_temp) + met[option][0] + " Weather: " + current_weather)
            else:
                day = current_day
                print("-------------------------------------------------------")
                print("Date: " + day)
                print("Time: " + current_time + " Temperature: " + str('%.1f' % current_temp) + met[option][0] + " Weather: " + current_weather)

    else:
        print("-------------------------------------------------------")
        print("Current Weather for " + CITY)
        #convert to centrigrade and set precision 1
        current_temp = response['main']['temp']
        current_wind_speed = response['wind']['speed']
        current_weather = response['weather'][0]['main']
        current_feels_like = response['main']['feels_like']
        current_humidity = response['main']['humidity']
        current_temp_min = response['main']['temp_min']
        current_temp_max = response['main']['temp_max']
        
        print("Temperature: " + str('%.1f' % current_temp) + met[option][0])
        print("Wind Speed: " + str('%.1f' % current_wind_speed) + met[option][1])
        print("Weather: " + current_weather)
        #print other conditions including feels like,humidity, temp_min, temp_max
        print("Feels Like: " + str('%.1f' % current_feels_like) + met[option][0])
        print("Humidity: " + str(current_humidity) + "%")
        print("Minimum Temperature: " + str('%.1f' %  current_temp_min) + met[option][0])
        print("Maximum Temperature: " + str('%.1f' %  current_temp_max) + met[option][0])
        print("-------------------------------------------------------")


def run(response, city, option_flag):
    """Prints the weather with the given command-line option. Public entry point of this unit."""
    global option
    option = option_flag
    parseJSONforCITY(response, city)
