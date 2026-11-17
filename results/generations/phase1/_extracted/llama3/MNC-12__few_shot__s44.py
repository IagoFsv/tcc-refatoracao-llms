"""Command-line program that shows the weather of a city.

Public entry point: run(city). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import runpy
import sys

import requests
import argparse
from dataclasses import dataclass

@dataclass
class WeatherResponse:
    cod: int
    weather: list

@dataclass
class Weather:
    description: str

def call_api(city):
    # fetch the key from a config file
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['openweathermap']['api_key']
    base_url = config['openweathermap']['base_url']
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response_from_api = requests.get(complete_url)
    return WeatherResponse(**response_from_api.json())

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

    response = call_api(args.city)
    # check if valid city name is passed
    if response.cod != 200:
        print("Invalid city name")
        exit(1)
    # get the weather from the response
    weather = response.weather[0].description
    print(weather)
