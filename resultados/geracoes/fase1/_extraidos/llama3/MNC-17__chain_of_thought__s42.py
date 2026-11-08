def print_weather(weather):
    if weather is None:
        print("Error: Could not get weather")
        return

    city_name = weather["name"]
    weather_description = weather["weather"][0]["description"]
    print(f"The weather in {city_name} is {weather_description}")

def executar(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_weather(weather)
