option = '-c'

def parseJSONforCITY(response, CITY):
    '''
    Print only for key = main, key = wind speed and key = weather[main] in a pretty format
    '''

    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}

    if option == '-f' or option == '-F':
        print("5-day Forecast for " + CITY)
        print_forecast_by_day(response['list'])
    else:
        print("-------------------------------------------------------")
        print("Current Weather for " + CITY)
        print_current_weather(response)

def print_forecast_by_day(forecast_list):
    day = ""
    for forecast in forecast_list:
        if day == forecast['dt_txt'][0:10]:
            print_weather_details(forecast)
        else:
            day = forecast['dt_txt'][0:10]
            print("-------------------------------------------------------")
            print("Date: " + day)
            print_weather_details(forecast)

def print_weather_details(forecast):
    print("Time: " + forecast['dt_txt'][11:16] + " Temperature: " + str('%.1f' % (forecast['main']['temp'])) + met[option][0] + " Weather: " + forecast['weather'][0]['main'])

def print_current_weather(response):
    print("Temperature: " + str('%.1f' % (response['main']['temp'])) + met[option][0])
    print("Wind Speed: " + str('%.1f' % (response['wind']['speed'])) + met[option][1])
    print("Weather: " + response['weather'][0]['main'])
    print("Feels Like: " + str('%.1f' % (response['main']['feels_like'])) + met[option][0])
    print("Humidity: " + str(response['main']['humidity']) + "%")
    print("Minimum Temperature: " + str('%.1f' %  (response['main']['temp_min'])) + met[option][0])
    print("Maximum Temperature: " + str('%.1f' %  (response['main']['temp_max'])) + met[option][0])
    print("-------------------------------------------------------")


def executar(response, cidade, opcao):
    """Imprime o clima com a opcao de linha de comando dada. Ponto de entrada publico desta unidade."""
    global option
    option = opcao
    parseJSONforCITY(response, cidade)
