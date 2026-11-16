import runpy
import sys

import requests
import argparse

def call_api(city):
    """Chama a API do OpenWeatherMap e retorna a resposta em formato JSON."""
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['openweathermap']['api_key']
    base_url = config['openweathermap']['base_url']
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response_from_api = requests.get(complete_url)
    return response_from_api.json()

def validate_city_response(response):
    """Valida a resposta da API e retorna True se a cidade é válida, False caso contrário."""
    if response['cod'] != 200:
        print("Invalid city name")
        return False
    return True

def get_weather_description(response):
    """Obtém a descrição do clima da resposta da API."""
    return response['weather'][0]['description']

def executar(cidade):
    """Roda este arquivo como programa, com a cidade na linha de comando. Ponto de entrada público desta unidade."""
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
    
    # Verifica se a cidade foi passada como argumento
    if args.city is None:
        print("Please provide city name")
        exit(1)
    
    response = call_api(args.city)
    
    # Valida a resposta da API
    if not validate_city_response(response):
        exit(1)
    
    # Obtém a descrição do clima
    weather = get_weather_description(response)
    
    # Exibe a descrição do clima
    print(weather)
