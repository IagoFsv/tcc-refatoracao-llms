"""Weather forecast of a city, printed on the terminal.

Public entry point: run(response, city, option_flag). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class Weather:
    main: str

@dataclass
class Main:
    temp: float
    feels_like: float
    humidity: int
    temp_min: float
    temp_max: float
    weather: Weather

@dataclass
class Wind:
    speed: float

@dataclass
class ListItem:
    dt_txt: str
    main: Main
    weather: Weather
    wind: Wind

@dataclass
class ResponseData:
    list: List[ListItem] = field(default_factory=list)

option = '-c'

def parseJSONforCITY(response: ResponseData, CITY: str):
    '''
    print only for key = main, key = wind speed and key = weather[main] in a pretty format
    '''

    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}

    if option == '-f' or option == '-F':
        print("5-day Forecast for " + CITY)
        day = ""
        for i in range(0, len(response.list)):
            if day == response.list[i].dt_txt[0:10]:
                print("Time: " + response.list[i].dt_txt[11:16] + " Temperature: " + str('%.1f' % (response.list[i].main.temp)) + met[option][0] + " Weather: " + response.list[i].weather.main)
            else:
                day = response.list[i].dt_txt[0:10]
                print("-------------------------------------------------------")
                print("Date: " + day)
                print("Time: " + response.list[i].dt_txt[11:16] + " Temperature: " + str('%.1f' % (response.list[i].main.temp)) + met[option][0] + " Weather: " + response.list[i].weather.main)             

    else:
        print("-------------------------------------------------------")
        print("Current Weather for " + CITY)
        print("Temperature: " + str('%.1f' % (response.main.temp)) + met[option][0])
        print("Wind Speed: " + str('%.1f' % (response.wind.speed)) + met[option][1])
        print("Weather: " + response.main.weather.main)
        print("Feels Like: " + str('%.1f' % (response.main.feels_like)) + met[option][0])
        print("Humidity: " + str(response.main.humidity) + "%")
        print("Minimum Temperature: " + str('%.1f' % (response.main.temp_min)) + met[option][0])
        print("Maximum Temperature: " + str('%.1f' % (response.main.temp_max)) + met[option][0])
        print("-------------------------------------------------------")


def run(response, city, option_flag):
    """Prints the weather with the given command-line option. Public entry point of this unit."""
    global option
    option = option_flag
    parseJSONforCITY(response, city)
