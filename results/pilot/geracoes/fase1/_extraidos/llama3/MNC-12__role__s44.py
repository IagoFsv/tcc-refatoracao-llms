import runpy
import sys
import argparse
import requests
import configparser

def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def fetch_weather(city):
    config = get_config()
    api_key = config['openweathermap']['api_key']
    base_url = config['openweathermap']['base_url']
    complete_url = f"{base_url}appid={api_key}&q={city}"
    response = requests.get(complete_url)
    return response.json()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name to get weather data")
    args = parser.parse_args()
    if args.city is None:
        print("Please provide city name")
        exit(1)
    response = fetch_weather(args.city)
    if response['cod'] != 200:
        print("Invalid city name")
        exit(1)
    weather = response['weather'][0]['description']
    print(weather)

if __name__ == '__main__':
    sys.argv = [__file__]
    runpy.run_path(__file__, run_name='__main__')
