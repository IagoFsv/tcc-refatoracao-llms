Clima atual de uma cidade, impresso no terminal.

Ponto de entrada publico: executar(weather). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

def print_weather(weather):
    if weather is not None:
        city_name = get_city_name(weather)
        weather_description = get_weather_description(weather)
        print(f"The weather in {city_name} is {weather_description}")
    else:
        print("Error: Could not get weather")

def get_city_name(weather):
    return weather["name"]

def get_weather_description(weather):
    return weather["weather"][0]["description"]

def executar(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_weather(weather)
