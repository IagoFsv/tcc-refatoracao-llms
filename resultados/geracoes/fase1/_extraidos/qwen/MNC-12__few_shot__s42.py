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
    response = requests.get(complete_url)
    return response.json()

def get_weather_data(city):
    response = call_api(city)
    if response['cod'] != 200:
        print("Invalid city name")
        exit(1)
    return response['weather'][0]['description']

def executar(cidade):
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name to get weather data")
    args = parser.parse_args()
    if args.city is None:
        print("Please provide city name")
        exit(1)
    
    weather = get_weather_data(args.city)
    print(weather)

if __name__ == '__main__':
    argv_anterior = sys.argv
    sys.argv = [__file__, ' '.join(sys.argv[1:])]
    try:
        runpy.run_path(__file__, run_name='__main__')
    finally:
        sys.argv = argv_anterior
