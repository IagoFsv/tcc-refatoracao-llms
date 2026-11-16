from dataclasses import dataclass

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
    weather: Weather
    wind: Wind

@dataclass
class Response:
    list: list
    main: Main
    wind: Wind
    weather: Weather

def parseJSONforCITY(response: Response, CITY: str):
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
        print("Weather: " + response.weather.main)
        print("Feels Like: " + str('%.1f' % (response.main.feels_like)) + met[option][0])
        print("Humidity: " + str(response.main.humidity) + "%")
        print("Minimum Temperature: " + str('%.1f' % (response.main.temp_min)) + met[option][0])
        print("Maximum Temperature: " + str('%.1f' % (response.main.temp_max)) + met[option][0])
        print("-------------------------------------------------------")

def executar(response, cidade, opcao):
    global option
    option = opcao
    parseJSONforCITY(response, cidade)
