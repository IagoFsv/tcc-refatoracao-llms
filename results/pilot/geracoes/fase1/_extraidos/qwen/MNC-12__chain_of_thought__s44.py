import runpy
import sys

import requests
import argparse

def call_api(city):
    # fetch the key from a config file
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['openweathermap']['api_key']
    base_url = config['openweathermap']['base_url']
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response_from_api = requests.get(complete_url)
    return response_from_api.json()

def executar(city):
    """Processa os argumentos da linha de comando e chama a função principal."""
    response = call_api(city)
    if response['cod'] != 200:
        print("Invalid city name")
        exit(1)
    weather = response['weather'][0]['description']
    print(weather)

def executar_script():
    """Roda este arquivo como programa, com a cidade na linha de comando. Ponto de entrada publico desta unidade."""
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name to get weather data")
    args = parser.parse_args()
    if args.city is None:
        print("Please provide city name")
        exit(1)
    executar(args.city)

if __name__ == '__main__':
    executar_script()
