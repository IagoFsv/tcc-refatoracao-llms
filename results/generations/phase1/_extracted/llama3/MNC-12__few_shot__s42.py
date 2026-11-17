"""Command-line program that shows the weather of a city.

Public entry point: run(city). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import runpy
import sys
import argparse
import requests
import configparser

import dataclasses

@dataclasses.dataclass
class WeatherResponse:
    cod: int
    weather: list

@dataclasses.dataclass
class Weather:
    description: str

@dataclasses.dataclass
class CityWeather:
    city: str
    weather: Weather

@dataclasses.dataclass
class OpenWeatherMapConfig:
    api_key: str
    base_url: str

def call_api(city: str, config: OpenWeatherMapConfig) -> WeatherResponse:
    complete_url = config.base_url + "appid=" + config.api_key + "&q=" + city
    response_from_api = requests.get(complete_url)
    return response_from_api.json()

def run(city: str):
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

    config = configparser.ConfigParser()
    config.read('config.ini')
    config_data = config['openweathermap']
    config = OpenWeatherMapConfig(api_key=config_data['api_key'], base_url=config_data['base_url'])

    response = call_api(args.city, config)
    # check if valid city name is passed
    if response['cod'] != 200:
        print("Invalid city name")
        exit(1)
    # get the weather from the response
    weather = Weather(description=response['weather'][0]['description'])
    city_weather = CityWeather(city=args.city, weather=weather)
    print(city_weather.weather.description)
