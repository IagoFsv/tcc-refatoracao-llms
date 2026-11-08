def print_weather(weather):
    if weather is not None:
        print(f"The weather in {weather['name']} is {weather['weather'][0]['description']}")

def executar(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_weather(weather)
