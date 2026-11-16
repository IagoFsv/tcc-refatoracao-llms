from dataclasses import dataclass

@dataclass
class WeatherCondition:
    main: str

@dataclass
class WindSpeed:
    speed: float

@dataclass
class Temperature:
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float

@dataclass
class CurrentWeather:
    temperature: Temperature
    wind_speed: WindSpeed
    humidity: int
    weather: WeatherCondition

@dataclass
class Forecast:
    date: str
    time: str
    temperature: float
    weather: WeatherCondition

def parse_json_for_city(response, cidade):
    if opcao in ['-f', '-F', '-c', '-C']:
        print(f"5-day Forecast for {cidade}")
        for forecast in response['list']:
            if opcao in ['-f', '-F', '-c', '-C']:
                print(f"Time: {forecast['dt_txt'][11:16]} Temperature: {forecast['main']['temp']:.1f}{met[opcao][0]} Weather: {forecast['weather'][0]['main']}")
            else:
                print(f"-------------------------------------------------------")
                print(f"Date: {forecast['dt_txt'][0:10]}")
                print(f"Time: {forecast['dt_txt'][11:16]} Temperature: {forecast['main']['temp']:.1f}{met[opcao][0]} Weather: {forecast['weather'][0]['main']}")
    else:
        print(f"-------------------------------------------------------")
        print(f"Current Weather for {cidade}")
        print(f"Temperature: {response['main']['temp']:.1f}{met[opcao][0]}")
        print(f"Wind Speed: {response['wind']['speed']:.1f}{met[opcao][1]}")
        print(f"Weather: {response['weather'][0]['main']}")
        print(f"Feels Like: {response['main']['feels_like']:.1f}{met[opcao][0]}")
        print(f"Humidity: {response['main']['humidity']}%")
        print(f"Minimum Temperature: {response['main']['temp_min']:.1f}{met[opcao][0]}")
        print(f"Maximum Temperature: {response['main']['temp_max']:.1f}{met[opcao][0]}")
        print(f"-------------------------------------------------------")


def executar(response, cidade, opcao):
    global option
    option = opcao
    parse_json_for_city(response, cidade)
