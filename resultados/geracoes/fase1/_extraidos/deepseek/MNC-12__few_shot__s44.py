"""Programa de linha de comando que mostra o clima de uma cidade.

Ponto de entrada publico: executar(cidade). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

import runpy
import sys

import requests
import argparse


def ler_configuracao():
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']


def chamar_api(config, city):
    base_url = config['base_url']
    api_key = config['api_key']
    complete_url = f"{base_url}?appid={api_key}&q={city}"
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name to get weather data")
    args = parser.parse_args()
    # check if city is passed as argument
    if args.city is None:
        print("Please provide city name")
        exit(1)

    config = ler_configuracao()
    response = chamar_api(config, args.city)
    # check if valid city name is passed
    if response['cod'] != 200:
        print("Invalid city name")
        exit(1)
    # get the weather from the response
    weather = response['weather'][0]['description']
    print(weather)
