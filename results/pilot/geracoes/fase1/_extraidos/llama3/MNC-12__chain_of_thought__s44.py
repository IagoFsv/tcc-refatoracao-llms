import runpy
import sys
import argparse

import requests
import configparser

def execute_file(file_path, city):
    sys.argv = [file_path, city]
    runpy.run_path(file_path, run_name='__main__')

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name to get weather data")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    if args.city is None:
        print("Please provide city name")
        exit(1)

    response = call_api(args.city)
    if response['cod'] != 200:
        print("Invalid city name")
        exit(1)
    weather = response['weather'][0]['description']
    print(weather)
