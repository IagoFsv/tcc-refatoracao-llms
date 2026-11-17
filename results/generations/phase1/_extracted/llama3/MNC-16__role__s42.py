"""Weather forecast of a city, printed on the terminal.

Public entry point: run(response, city, option_flag). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

option = '-c'

def parseJSONforCITY(response, city):
    '''
    print only for key = main, key = wind speed and key = weather[main] in a pretty format
    '''

    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}

    if option in ['-f', '-F', '-c', '-C']:
        print("5-day Forecast for " + city)
        """check for date field
           if the day is same, print the content in the same line
           if the day is different, print the content in the next line
        """
        day = ""
        for forecast in response['list']:
            if day == forecast['dt_txt'][:10]:
                print(f"Time: {forecast['dt_txt'][11:16]} Temperature: {str('%.1f' % (forecast['main']['temp']))} {met[option][0]} Weather: {forecast['weather'][0]['main']}")
            else:
                day = forecast['dt_txt'][:10]
                print("-------------------------------------------------------")
                print(f"Date: {day}")
                print(f"Time: {forecast['dt_txt'][11:16]} Temperature: {str('%.1f' % (forecast['main']['temp']))} {met[option][0]} Weather: {forecast['weather'][0]['main']}")             

    else:
        print("-------------------------------------------------------")
        print("Current Weather for " + city)
        #convert to centrigrade and set precision 1
        print(f"Temperature: {str('%.1f' % (response['main']['temp']))} {met[option][0]}")
        print(f"Wind Speed: {str('%.1f' % (response['wind']['speed']))} {met[option][1]}")
        print(f"Weather: {response['weather'][0]['main']}")
        #print other conditions including feels like,humidity, temp_min, temp_max
        print(f"Feels Like: {str('%.1f' % (response['main']['feels_like']))} {met[option][0]}")
        print(f"Humidity: {str(response['main']['humidity'])}%")
        print(f"Minimum Temperature: {str('%.1f' %  (response['main']['temp_min']))} {met[option][0]}")
        print(f"Maximum Temperature: {str('%.1f' %  (response['main']['temp_max']))} {met[option][0]}")
        print("-------------------------------------------------------")


def run(response, city, option_flag):
    """Prints the weather with the given command-line option. Public entry point of this unit."""
    global option
    option = option_flag
    parseJSONforCITY(response, city)
