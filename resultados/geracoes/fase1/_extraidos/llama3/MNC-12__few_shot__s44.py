from dataclasses import dataclass
from typing import List
import configparser
import requests
import argparse
import sys

@dataclass
class WeatherResponse:
    cod: int
    weather: List[dict]

@dataclass
class Weather:
    description: str

@dataclass
class CityWeather:
    city: str
    weather: Weather

def call_api(city: str) -> WeatherResponse:
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['openweathermap']['api_key']
    base_url = config['openweathermap']['base_url']
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response_from_api = requests.get(complete_url)
    return WeatherResponse(**response_from_api.json())

def get_weather(city: str) -> CityWeather:
    response = call_api(city)
    if response.cod != 200:
        print("Invalid city name")
        exit(1)
    weather = Weather(description=response.weather[0]['description'])
    return CityWeather(city, weather)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name to get weather data")
    args = parser.parse_args()
    if args.city is None:
        print("Please provide city name")
        exit(1)
    city_weather = get_weather(args.city)
    print(city_weather.weather.description)
