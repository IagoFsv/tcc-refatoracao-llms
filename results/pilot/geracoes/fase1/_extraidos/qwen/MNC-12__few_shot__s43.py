import runpy
import sys
import requests
import argparse
import configparser

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    @property
    def api_key(self):
        return self.config['openweathermap']['api_key']

    @property
    def base_url(self):
        return self.config['openweathermap']['base_url']

class WeatherAPI:
    def __init__(self, config):
        self.config = config

    def call_api(self, city):
        complete_url = f"{self.config.base_url}appid={self.config.api_key}&q={city}"
        response_from_api = requests.get(complete_url)
        return response_from_api.json()

class WeatherApp:
    def __init__(self):
        self.config = Config()
        self.weather_api = WeatherAPI(self.config)

    def executar(self, cidade):
        argv_anterior = sys.argv
        sys.argv = [__file__, cidade]
        try:
            runpy.run_path(__file__, run_name='__main__')
        finally:
            sys.argv = argv_anterior

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("city", help="City name to get weather data")
        args = parser.parse_args()
        if args.city is None:
            print("Please provide city name")
            return 1

        response = self.weather_api.call_api(args.city)
        if response['cod'] != 200:
            print("Invalid city name")
            return 1

        weather = response['weather'][0]['description']
        print(weather)
        return 0

if __name__ == '__main__':
    app = WeatherApp()
    sys.exit(app.run())
