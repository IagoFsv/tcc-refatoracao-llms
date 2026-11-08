from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class OpenWeatherMapConfig:
    api_key: str
    base_url: str

@dataclass
class WeatherResponse:
    cod: int
    weather: List[Dict[str, Any]]

@dataclass
class WeatherData:
    description: str

def call_api(city: str, config: OpenWeatherMapConfig) -> WeatherResponse:
    complete_url = config.base_url + "appid=" + config.api_key + "&q=" + city
    response_from_api = requests.get(complete_url)
    return response_from_api.json()

def executar(cidade: str):
    """Roda este arquivo como programa, com a cidade na linha de comando. Ponto de entrada publico desta unidade."""
    argv_anterior = sys.argv
    sys.argv = [__file__, cidade]
    try:
        runpy.run_path(__file__, run_name='__main__')
    finally:
        sys.argv = argv_anterior

    config = OpenWeatherMapConfig(**configparser.ConfigParser().read('config.ini')['openweathermap'])
    response = call_api(cidade, config)
    if response['cod'] != 200:
        print("Invalid city name")
        exit(1)
    weather = WeatherData(description=response['weather'][0]['description'])
    print(weather.description)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("city", help="City name to get weather data")
    args = parser.parse_args()
    if args.city is None:
        print("Please provide city name")
        exit(1)
    executar(args.city)
