"""Command-line program that shows the weather of a city.

Public entry point: run(city). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import runpy
import sys
import argparse
import requests
import configparser

import WeatherAPI

class WeatherAPIResponse:
    def __init__(self, api_response):
        self.api_response = api_response

    @property
    def weather(self):
        return self.api_response['weather'][0]['description']

class WeatherAPI:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def call_api(self, city):
        complete_url = self.base_url + "appid=" + self.api_key + "&q=" + city
        response_from_api = requests.get(complete_url)
        return WeatherAPIResponse(response_from_api.json())

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

    api_key = configparser.ConfigParser()
    api_key.read('config.ini')
    api_key = api_key['openweathermap']['api_key']
    base_url = api_key['openweathermap']['base_url']

    weather_api = WeatherAPI(api_key, base_url)
    response = weather_api.call_api(args.city)
    # check if valid city name is passed
    if response.api_response['cod'] != 200:
        print("Invalid city name")
        exit(1)
    # get the weather from the response
    print(response.weather)
