"""Weather forecast of a city, printed on the terminal.

Public entry point: run(response, city, option_flag). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

from typing import Dict, Any

class Weather:
    def __init__(self, response: Dict[str, Any]):
        self.response = response

    def parseJSONforCITY(self, CITY: str, option: str):
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
            for i in range(0, len(self.response['list'])):
                if day == self.response['list'][i]['dt_txt'][0:10]:
                    print("Time: " + self.response['list'][i]['dt_txt'][11:16] + 
                          " Temperature: " + str('%.1f' % (self.response['list'][i]['main']['temp'])) + 
                          met[option][0] + 
                          " Weather: " + self.response['list'][i]['weather'][0]['main'])
                else:
                    day = self.response['list'][i]['dt_txt'][0:10]
                    print("-------------------------------------------------------")
                    print("Date: " + day)
                    print("Time: " + self.response['list'][i]['dt_txt'][11:16] + 
                          " Temperature: " + str('%.1f' % (self.response['list'][i]['main']['temp'])) + 
                          met[option][0] + 
                          " Weather: " + self.response['list'][i]['weather'][0]['main'])             

        else:
            print("-------------------------------------------------------")
            print("Current Weather for " + CITY)
            #convert to centrigrade and set precision 1
            print("Temperature: " + str('%.1f' % (self.response['main']['temp'])) + met[option][0])
            print("Wind Speed: " + str('%.1f' % (self.response['wind']['speed'])) + met[option][1])
            print("Weather: " + self.response['weather'][0]['main'])
            #print other conditions including feels like,humidity, temp_min, temp_max
            print("Feels Like: " + str('%.1f' % (self.response['main']['feels_like'])) + met[option][0])
            print("Humidity: " + str(self.response['main']['humidity']) + "%")
            print("Minimum Temperature: " + str('%.1f' %  (self.response['main']['temp_min'])) + met[option][0])
            print("Maximum Temperature: " + str('%.1f' %  (self.response['main']['temp_max'])) + met[option][0])
            print("-------------------------------------------------------")


def run(response: Dict[str, Any], city: str, option_flag: str):
    """Prints the weather with the given command-line option. Public entry point of this unit."""
    weather = Weather(response)
    weather.parseJSONforCITY(city, option_flag)
