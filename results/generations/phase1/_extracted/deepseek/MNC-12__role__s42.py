"""Command-line program that shows the weather of a city.

Public entry point: run(city). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import runpy
import sys
import requests
import argparse
import configparser


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api_key'], config['openweathermap']['base_url']


def call_api(city, api_key, base_url):
    complete_url = f"{base_url}appid={api_key}&q={city}"
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


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name to get weather data")
    return parser.parse_args()


if __name__ == '__main__':
    api_key, base_url = get_api_key()
    args = parse_arguments()
    if args.city is None:
        print("Please provide city name")
        exit(1)

    response = call_api(args.city, api_key, base_url)
    if response['cod'] != 200:
        print("Invalid city name")
        exit(1)

    weather = response['weather'][0]['description']
    print(weather)
