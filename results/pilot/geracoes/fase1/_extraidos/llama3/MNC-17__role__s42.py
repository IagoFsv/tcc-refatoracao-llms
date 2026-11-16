from typing import Optional

def print_weather(weather: Optional[dict]) -> None:
    if weather is not None:
        print(f"The weather in {weather['name']} is {weather['weather'][0]['description']}")
    else:
        print("Error: Could not get weather")

def executar(weather: Optional[dict]) -> None:
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_weather(weather)
