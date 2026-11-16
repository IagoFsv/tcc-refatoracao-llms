def format_weather_message(weather):
    if weather is None:
        return "Error: Could not get weather"
    else:
        return f"The weather in {weather['name']} is {weather['weather'][0]['description']}"

def print_weather(weather):
    message = format_weather_message(weather)
    print(message)

def executar(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_weather(weather)
