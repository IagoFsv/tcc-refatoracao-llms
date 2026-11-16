def print_weather(weather_data, city):
    """Imprime a previsão do tempo"""
    print("-------------------------------------------------------")
    print("Current Weather for " + city)
    print("Temperature: " + str('%.1f' % (weather_data['main']['temp'])) + weather_data['units'][0])
    print("Wind Speed: " + str('%.1f' % (weather_data['wind']['speed'])) + weather_data['units'][1])
    print("Weather: " + weather_data['weather'][0]['main'])
    print("Feels Like: " + str('%.1f' % (weather_data['main']['feels_like'])) + weather_data['units'][0])
    print("Humidity: " + str(weather_data['main']['humidity']) + "%")
    print("Minimum Temperature: " + str('%.1f' % (weather_data['main']['temp_min'])) + weather_data['units'][0])
    print("Maximum Temperature: " + str('%.1f' % (weather_data['main']['temp_max'])) + weather_data['units'][0])
    print("-------------------------------------------------------")

def parse_weather(response, city, option):
    """Parseia a resposta do JSON e prepara os dados para impressão"""
    weather_data = response['main']
    weather_data['units'] = met[option]
    return weather_data

def executar(response, cidade, opcao):
    """Imprime o clima com a opcao de linha de comando dada"""
    global option
    option = opcao
    weather_data = parse_weather(response, cidade, option)
    print_weather(weather_data, cidade)
