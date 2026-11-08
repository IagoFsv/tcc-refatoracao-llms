from dataclasses import dataclass

@dataclass
class WeatherCondition:
    main: str
    dt_txt: str

@dataclass
class WeatherForecast:
    date: str
    time: str
    temperature: float
    weather: WeatherCondition

@dataclass
class CurrentWeather:
    temperature: float
    wind_speed: float
    humidity: int
    feels_like: float
    temp_min: float
    temp_max: float
    weather: WeatherCondition

def parseJSONforCITY(response, cidade):
    if option == '-f' or option == '-F':
        print("5-day Forecast for " + cidade)
        for forecast in response['list']:
            if day == forecast['dt_txt'][0:10]:
                print("Time: " + forecast['dt_txt'][11:16] + " Temperature: " + str('%.1f' % forecast['main']['temp']) + met[option][0] + " Weather: " + forecast['weather'][0]['main'])
            else:
                day = forecast['dt_txt'][0:10]
                print("-------------------------------------------------------")
                print("Date: " + day)
                print("Time: " + forecast['dt_txt'][11:16] + " Temperature: " + str('%.1f' % forecast['main']['temp']) + met[option][0] + " Weather: " + forecast['weather'][0]['main'])             

    else:
        print("-------------------------------------------------------")
        print("Current Weather for " + cidade)
        current_weather = CurrentWeather(
            temperature=str('%.1f' % response['main']['temp']) + met[option][0],
            wind_speed=str('%.1f' % response['wind']['speed']) + met[option][1],
            humidity=response['main']['humidity'],
            feels_like=str('%.1f' % response['main']['feels_like']) + met[option][0],
            temp_min=str('%.1f' % response['main']['temp_min']) + met[option][0],
            temp_max=str('%.1f' % response['main']['temp_max']) + met[option][0],
            weather=response['weather'][0]
        )
        print("Temperature: " + current_weather.temperature)
        print("Wind Speed: " + current_weather.wind_speed)
        print("Weather: " + current_weather.weather.main)
        print("Feels Like: " + current_weather.feels_like)
        print("Humidity: " + str(current_weather.humidity) + "%")
        print("Minimum Temperature: " + current_weather.temp_min)
        print("Maximum Temperature: " + current_weather.temp_max)
        print("-------------------------------------------------------")


def executar(response, cidade, opcao):
    global option
    option = opcao
    parseJSONforCITY(response, cidade)
