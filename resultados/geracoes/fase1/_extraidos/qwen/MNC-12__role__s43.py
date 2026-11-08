import runpy
import sys
import requests
import argparse
import configparser

def call_api(city):
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['openweathermap']['api_key']
    base_url = config['openweathermap']['base_url']
    complete_url = f"{base_url}appid={api_key}&q={city}"
    response_from_api = requests.get(complete_url)
    return response_from_api.json()

def get_weather_data(city):
    response = call_api(city)
    if response['cod'] != 200:
        raise ValueError("Invalid city name")
    weather = response['weather'][0]['description']
    return weather

def executar(cidade):
    argv_anterior = sys.argv
    sys.argv = [__file__, cidade]
    try:
        runpy.run_path(__file__, run_name='__main__')
    finally:
        sys.argv = argv_anterior

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name to get weather data")
    args = parser.parse_args()

    if args.city is None:
        print("Please provide city name")
        exit(1)

    try:
        weather = get_weather_data(args.city)
        print(weather)
    except ValueError as e:
        print(e)
        exit(1)
