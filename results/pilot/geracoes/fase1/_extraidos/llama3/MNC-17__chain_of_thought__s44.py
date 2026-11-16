class CityWeather:
    def __init__(self, name, description):
        self.name = name
        self.description = description

def print_weather(weather):
    if weather is not None:
        print(f"The weather in {weather.name} is {weather.description}")
    else:
        print("Error: Could not get weather")


def executar(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_weather(CityWeather(**weather))
