def get_city_name(weather):
    if weather is not None:
        return weather["name"]
    else:
        return None

def get_weather_description(weather):
    if weather is not None:
        return weather["weather"][0]["description"]
    else:
        return None

def print_weather(weather):
    city_name = get_city_name(weather)
    weather_description = get_weather_description(weather)
    
    if city_name is not None and weather_description is not None:
        print("The weather in " + city_name + " is " + weather_description)
    else:
        print("Error: Could not get weather")


def executar(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_weather(weather)
