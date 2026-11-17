class WeatherData:
    def __init__(self, json_response):
        self.main = Main(json_response['main'])
        self.weather = Weather(json_response['weather'][0])
        self.wind = Wind(json_response['wind'])
        self.clouds = Clouds(json_response['clouds'])
        self.sys = System(json_response['sys'])

class Main:
    def __init__(self, main_data):
        self.temp = round(main_data['temp'] - 273.15)
        self.humidity = main_data['humidity']
        self.pressure = main_data['pressure']

class Weather:
    def __init__(self, weather_data):
        self.main = weather_data['main']
        self.icon = weather_data['icon']

class Wind:
    def __init__(self, wind_data):
        self.speed = wind_data['speed']

class Clouds:
    def __init__(self, clouds_data):
        self.all = clouds_data['all']

class System:
    def __init__(self, sys_data):
        self.country = sys_data['country']

# ... rest of the code remains the same
