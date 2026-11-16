from dataclasses import dataclass, field
from typing import List

@dataclass
class Main:
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int

@dataclass
class Wind:
    speed: float

@dataclass
class Weather:
    main: str

@dataclass
class ListItem:
    dt_txt: str
    main: Main
    wind: Wind
    weather: List[Weather] = field(default_factory=list)

@dataclass
class Response:
    list: List[ListItem] = field(default_factory=list)
    main: Main
    wind: Wind
    weather: List[Weather] = field(default_factory=list)

option = '-c'

def parseJSONforCITY(response: Response, CITY: str):
    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}

    if option == '-f' or option == '-F':
        print("5-day Forecast for " + CITY)
        day = ""
        for i in range(0, len(response.list)):
            if day == response.list[i].dt_txt[0:10]:
                print("Time: " + response.list[i].dt_txt[11:16] + " Temperature: " + str('%.1f' % (response.list[i].main.temp)) + met[option][0] + " Weather: " + response.list[i].weather[0].main)
            else:
                day = response.list[i].dt_txt[0:10]
                print("-------------------------------------------------------")
                print("Date: " + day)
                print("Time: " + response.list[i].dt_txt[11:16] + " Temperature: " + str('%.1f' % (response.list[i].main.temp)) + met[option][0] + " Weather: " + response.list[i].weather[0].main)             

    else:
        print("-------------------------------------------------------")
        print("Current Weather for " + CITY)
        print("Temperature: " + str('%.1f' % (response.main.temp)) + met[option][0])
        print("Wind Speed: " + str('%.1f' % (response.wind.speed)) + met[option][1])
        print("Weather: " + response.weather[0].main)
        print("Feels Like: " + str('%.1f' % (response.main.feels_like)) + met[option][0])
        print("Humidity: " + str(response.main.humidity) + "%")
        print("Minimum Temperature: " + str('%.1f' % (response.main.temp_min)) + met[option][0])
        print("Maximum Temperature: " + str('%.1f' % (response.main.temp_max)) + met[option][0])
        print("-------------------------------------------------------")


def executar(response: Response, cidade: str, opcao: str):
    global option
    option = opcao
    parseJSONforCITY(response, cidade)
