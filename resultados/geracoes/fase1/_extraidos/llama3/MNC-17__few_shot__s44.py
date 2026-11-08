from dataclasses import dataclass

@dataclass
class Weather:
    name: str
    weather: list[dict[str, str]]

def print_weather(weather: Weather):
    if weather is not None:
        print(f"The weather in {weather.name} is {weather.weather[0]['description']}")
    else:
        print("Error: Could not get weather")

def executar(weather: Weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_weather(weather)
