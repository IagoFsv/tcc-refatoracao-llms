def print_city_name(weather):
    if weather is not None:
        print("The weather in " + weather["name"], end=" ")
    else:
        print("Error: Could not get weather", end=" ")


def print_weather_description(weather):
    if weather is not None:
        print(weather["weather"][0]["description"])
    else:
        print("Could not get weather")


def print_weather(weather):
    print_city_name(weather)
    print_weather_description(weather)


def executar(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_weather(weather)
