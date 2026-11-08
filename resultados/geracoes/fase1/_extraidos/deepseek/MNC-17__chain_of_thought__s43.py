"""Clima atual de uma cidade, impresso no terminal.

Ponto de entrada publico: executar(weather). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

def print_weather_error():
    print("Error: Could not get weather")


def print_weather_info(weather):
    print("The weather in " + weather["name"] + " is " + weather["weather"][0]["description"])


def executar(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    if weather is None:
        print_weather_error()
    else:
        print_weather_info(weather)
