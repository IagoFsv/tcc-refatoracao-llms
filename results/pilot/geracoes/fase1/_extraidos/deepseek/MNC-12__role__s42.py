"""Programa de linha de comando que mostra o clima de uma cidade.

Ponto de entrada publico: executar(cidade). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

import runpy
import sys
import requests
import argparse
import configparser


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def call_api(city, config):
    api_key = config['openweathermap']['api_key']
    base_url = config['openweathermap']['base_url']
    complete_url = f"{base_url}appid={api_key}&q={city}"
    response_from_api = requests.get(complete_url)
    return response_from_api.json()


def executar(cidade):
    """Roda este arquivo como programa, com a cidade na linha de comando. Ponto de entrada publico desta unidade."""
    argv_anterior = sys.argv
    sys.argv = [__file__, cidade]
    try:
        runpy.run_path(__file__, run_name='__main__')
    finally:
        sys.argv = argv_anterior


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name to get weather data")
    return parser.parse_args()


def validate_city(response):
    if response['cod'] != 200:
        print("Invalid city name")
        exit(1)


def get_weather(response):
    return response['weather'][0]['description']


if __name__ == '__main__':
    config = read_config()
    args = parse_arguments()
    if args.city is None:
        print("Please provide city name")
        exit(1)
    response = call_api(args.city, config)
    validate_city(response)
    weather = get_weather(response)
    print(weather)
