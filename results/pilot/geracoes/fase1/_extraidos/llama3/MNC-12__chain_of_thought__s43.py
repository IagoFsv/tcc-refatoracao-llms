import runpy
import sys
import argparse

def run_script(city):
    sys.argv = [__file__, city]
    runpy.run_path(__file__, run_name='__main__')

def execute_script(city):
    try:
        run_script(city)
    finally:
        sys.argv = [__file__]

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
