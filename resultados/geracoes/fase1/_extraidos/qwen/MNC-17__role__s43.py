def print_weather_details(weather):
    if weather is None:
        print("Error: Could not get weather")
    else:
        city_name = weather["name"]
        weather_description = weather["weather"][0]["description"]
        print(f"The weather in {city_name} is {weather_description}")

def executar(weather):
    """Imprime o clima recebido da API. Ponto de entrada publico desta unidade."""
    print_weather_details(weather)
