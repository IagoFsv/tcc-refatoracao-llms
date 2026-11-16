"""Previsao do tempo de uma cidade, impressa no terminal.

Ponto de entrada publico: executar(response, cidade, opcao). Nao altere o
nome nem a assinatura dessa funcao; o restante do arquivo pode ser
reorganizado livremente.
"""

TEMP_METRIC = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}

def parse_json_for_city(response, city, option):
    '''
    print only for key = main, key = wind speed and key = weather[main] in a pretty format
    '''
    print_current_weather(response, city, option)
    print_forecast(response, city, option)

def print_current_weather(response, city, option):
    print("-------------------------------------------------------")
    print("Current Weather for " + city)
    print_temperature(response, option)
    print_wind_speed(response, option)
    print("Weather: " + response['weather'][0]['main'])
    print_other_conditions(response, option)
    print("-------------------------------------------------------")

def print_forecast(response, city, option):
    if option == '-f' or option == '-F':
        print("5-day Forecast for " + city)
        print_forecast_details(response, option)

def print_temperature(response, option):
    print("Temperature: " + str('%.1f' % (response['main']['temp'])) + TEMP_METRIC[option][0])

def print_wind_speed(response, option):
    print("Wind Speed: " + str('%.1f' % (response['wind']['speed'])) + TEMP_METRIC[option][1])

def print_other_conditions(response, option):
    print("Feels Like: " + str('%.1f' % (response['main']['feels_like'])) + TEMP_METRIC[option][0])
    print("Humidity: " + str(response['main']['humidity']) + "%")
    print("Minimum Temperature: " + str('%.1f' % (response['main']['temp_min'])) + TEMP_METRIC[option][0])
    print("Maximum Temperature: " + str('%.1f' % (response['main']['temp_max'])) + TEMP_METRIC[option][0])

def print_forecast_details(response, option):
    day = ""
    for i in range(0, len(response['list'])):
        if day == response['list'][i]['dt_txt'][0:10]:
            print_forecast_item(response['list'][i], option)
        else:
            day = response['list'][i]['dt_txt'][0:10]
            print("-------------------------------------------------------")
            print("Date: " + day)
            print_forecast_item(response['list'][i], option)

def print_forecast_item(item, option):
    print("Time: " + item['dt_txt'][11:16] + " Temperature: " + str('%.1f' % (item['main']['temp'])) + TEMP_METRIC[option][0] + " Weather: " + item['weather'][0]['main'])

def executar(response, city, option):
    """Imprime o clima com a opcao de linha de comando dada. Ponto de entrada publico desta unidade."""
    parse_json_for_city(response, city, option)
