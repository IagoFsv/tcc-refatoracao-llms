Clima atual de uma cidade, impresso no terminal.

Ponto de entrada publico: executar(weather). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

def print_weather_description(weather):
    """Imprime a descrição do clima."""
    print("The weather in " + weather["name"] + " is " + weather["weather"][0]["description"])

def print_weather(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    if weather is not None:
        print_weather_description(weather)
    else:
        print("Error: Could not get weather")

def executar(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_weather(weather)
