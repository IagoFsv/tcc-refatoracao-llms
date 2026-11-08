from dataclasses import dataclass

@dataclass
class WeatherCondition:
    main: str

@dataclass
class Weather:
    weather: List[WeatherCondition]

@dataclass
class Wind:
    speed: float

@dataclass
class Main:
    temp: float
    feels_like: float
    humidity: int
    temp_min: float
    temp_max: float

@dataclass
class CityWeather:
    city: str
    weather: Weather
    wind: Wind
    main: Main

@dataclass
class Forecast:
    dt_txt: str
    main: Main
    weather: Weather

@dataclass
class CityForecast:
    city: str
    forecasts: List[Forecast]

def parseJSONforCITY(response, cidade):
    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}
    if met[opcao][0] == '°C':
        temp_format = '%.1f' % (response['main']['temp'])
    else:
        temp_format = '%.1f' % (response['main']['temp'] * 9/5 + 32)

    if opcao in ['-f', '-F', '-c', '-C']:
        print("5-day Forecast for " + cidade)
        for i in range(0, len(response['list'])):
            forecast = Forecast(dt_txt=response['list'][i]['dt_txt'], main=Main(temp=temp_format, feels_like=response['main']['feels_like'], humidity=response['main']['humidity'], temp_min=response['main']['temp_min'], temp_max=response['main']['temp_max']), weather=Weather(weather=[WeatherCondition(main=response['weather'][0]['main'])]))
            print("Time: " + response['list'][i]['dt_txt'][11:16] + " Temperature: " + temp_format + " Weather: " + response['list'][i]['weather'][0]['main'])
    else:
        print("-------------------------------------------------------")
        print("Current Weather for " + cidade)
        print("Temperature: " + temp_format + met[opcao][0])
        print("Wind Speed: " + str('%.1f' % (response['wind']['speed'])) + met[opcao][1])
        print("Weather: " + response['weather'][0]['main'])
        print("Feels Like: " + str('%.1f' % (response['main']['feels_like'])) + met[opcao][0])
        print("Humidity: " + str(response['main']['humidity']) + "%")
        print("Minimum Temperature: " + str('%.1f' %  (response['main']['temp_min'])) + met[opcao][0])
        print("Maximum Temperature: " + str('%.1f' %  (response['main']['temp_max'])) + met[opcao][0])
        print("-------------------------------------------------------")

def executar(response, cidade, opcao):
    global option
    option = opcao
    parseJSONforCITY(response, cidade)
