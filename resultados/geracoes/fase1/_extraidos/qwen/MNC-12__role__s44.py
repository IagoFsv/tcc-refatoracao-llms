import runpy
import sys
import requests
import argparse
import configparser

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api_key'], config['openweathermap']['base_url']

def call_api(city):
    api_key, base_url = get_api_key()
    complete_url = f"{base_url}appid={api_key}&q={city}"
    response_from_api = requests.get(complete_url)
    return response_from_api.json()

def execute_with_city(cidade):
    """Roda este arquivo como programa, com a cidade na linha de comando. Ponto de entrada publico desta unidade."""
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

    response = call_api(args.city)
    
    if response['cod'] != 200:
        print("Invalid city name")
        exit(1)

    weather = response['weather'][0]['description']
    print(weather)
