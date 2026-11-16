"""Clima atual de uma cidade, impresso no terminal.

Ponto de entrada publico: executar(weather). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

def print_weather(city_name, weather_description):
    if city_name and weather_description:
        print("The weather in " + city_name + " is " + weather_description)
    else:
        print("Error: Could not get weather")


def executar(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    city_name = weather["name"] if weather else None
    weather_description = weather["weather"][0]["description"] if weather else None
    print_weather(city_name, weather_description)
