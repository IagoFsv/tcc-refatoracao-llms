import runpy
import sys
import argparse

import requests
import configparser

def call_api(city):
    # fetch the key from a config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['openweathermap']['api_key']
    base_url = config['openweathermap']['base_url']
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response_from_api = requests.get(complete_url)
    return response_from_api.json()

def get_weather(city):
    response = call_api(city)
    if response['cod'] != 200:
        print("Invalid city name")
        return None
    weather = response['weather'][0]['description']
    return weather

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name to get weather data")
    args = parser.parse_args()
    if args.city is None:
        print("Please provide city name")
        exit(1)
    weather = get_weather(args.city)
    if weather is not None:
        print(weather)

if __name__ == '__main__':
    main()
