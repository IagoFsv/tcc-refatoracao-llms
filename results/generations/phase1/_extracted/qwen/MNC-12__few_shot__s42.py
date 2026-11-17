"""Command-line program that shows the weather of a city.

Public entry point: run(city). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import runpy
import sys
import requests
import argparse
import configparser


class WeatherConfig:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.api_key = self.config['openweathermap']['api_key']
        self.base_url = self.config['openweathermap']['base_url']

    def call_api(self, city):
        complete_url = f"{self.base_url}appid={self.api_key}&q={city}"
        response_from_api = requests.get(complete_url)
        return response_from_api.json()


def run(city):
    """Runs this file as a program, with the city on the command line. Public entry point of this unit."""
    previous_argv = sys.argv
    sys.argv = [__file__, city]
    try:
        runpy.run_path(__file__, run_name='__main__')
    finally:
        sys.argv = previous_argv


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name to get weather data")
    args = parser.parse_args()
    # check if city is passed as argument
    if args.city is None:
        print("Please provide city name")
        exit(1)

    weather_config = WeatherConfig('config.ini')
    response = weather_config.call_api(args.city)
    # check if valid city name is passed
    if response['cod'] != 200:
        print("Invalid city name")
        exit(1)
    # get the weather from the response
    weather = response['weather'][0]['description']
    print(weather)
