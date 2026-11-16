def get_city_name(weather):
    return weather["name"]

def get_weather_description(weather):
    return weather["weather"][0]["description"]

def print_weather(weather):
    city_name = get_city_name(weather)
    weather_description = get_weather_description(weather)
    if weather is not None:
        print(f"The weather in {city_name} is {weather_description}")
    else:
        print("Error: Could not get weather")

def executar(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_weather(weather)
