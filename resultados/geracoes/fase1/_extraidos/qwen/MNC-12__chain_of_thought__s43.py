import runpy
import sys
import requests
import argparse
import configparser

def read_config():
    # Lê a configuração do arquivo config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api_key'], config['openweathermap']['base_url']

def build_url(api_key, city):
    # Constrói a URL completa para a requisição à API
    base_url = read_config()[1]
    return f"{base_url}appid={api_key}&q={city}"

def fetch_weather(api_key, city):
    # Faz a requisição à API
    url = build_url(api_key, city)
    response_from_api = requests.get(url)
    return response_from_api.json()

def handle_response(response):
    # Analisa a resposta da API
    if response['cod'] != 200:
        print("Invalid city name")
        exit(1)
    weather = response['weather'][0]['description']
    return weather

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
    
    # Verifica se a cidade foi fornecida como argumento
    if args.city is None:
        print("Please provide city name")
        exit(1)
    
    api_key, base_url = read_config()
    response = fetch_weather(api_key, args.city)
    weather = handle_response(response)
    print(weather)
