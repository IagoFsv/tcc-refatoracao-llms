def print_weather(weather):
    """Imprime o clima recebido da API."""
    if weather is None:
        print("Error: Could not get weather")
    else:
        print(f"The weather in {weather['name']} is {weather['weather'][0]['description']}")

def executar(weather):
    """Ponto de entrada publico para imprimir o clima recebido da API."""
    print_weather(weather)
