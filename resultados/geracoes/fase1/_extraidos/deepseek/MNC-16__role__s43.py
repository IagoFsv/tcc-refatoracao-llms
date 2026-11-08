"""Previsao do tempo de uma cidade, impressa no terminal.

Ponto de entrada publico: executar(response, cidade, opcao). Nao altere o
nome nem a assinatura dessa funcao; o restante do arquivo pode ser
reorganizado livremente.
"""

option = '-c'

def parseJSONforCITY(response, CITY, met):
    '''
    print only for key = main, key = wind speed and key = weather[main] in a pretty format
    '''

    if option in ['-f', '-F']:
        print_forecast(response, CITY, met)
    else:
        print_current_weather(response, CITY, met)


def print_forecast(response, CITY, met):
    print("5-day Forecast for " + CITY)
    day = ""
    for i in range(0, len(response['list'])):
        if day == response['list'][i]['dt_txt'][0:10]:
            print_weather_info(response, i, met)
        else:
            day = response['list'][i]['dt_txt'][0:10]
            print_date(day)
            print_weather_info(response, i, met)


def print_current_weather(response, CITY, met):
    print("-------------------------------------------------------")
    print("Current Weather for " + CITY)
    print_temperature(response, met)
    print_wind_speed(response, met)
    print("Weather: " + response['weather'][0]['main'])
    print_other_conditions(response, met)
    print("-------------------------------------------------------")


def print_weather_info(response, i, met):
    print("Time: " + response['list'][i]['dt_txt'][11:16] + " Temperature: " + 
          str('%.1f' % (response['list'][i]['main']['temp'])) + met[option][0] + 
          " Weather: " + response['list'][i]['weather'][0]['main'])


def print_date(day):
    print("-------------------------------------------------------")
    print("Date: " + day)


def print_temperature(response, met):
    print("Temperature: " + str('%.1f' % (response['main']['temp'])) + met[option][0])


def print_wind_speed(response, met):
    print("Wind Speed: " + str('%.1f' % (response['wind']['speed'])) + met[option][1])


def print_other_conditions(response, met):
    print("Feels Like: " + str('%.1f' % (response['main']['feels_like'])) + met[option][0])
    print("Humidity: " + str(response['main']['humidity']) + "%")
    print("Minimum Temperature: " + str('%.1f' % (response['main']['temp_min'])) + met[option][0])
    print("Maximum Temperature: " + str('%.1f' % (response['main']['temp_max'])) + met[option][0])


def executar(response, cidade, opcao):
    """Imprime o clima com a opcao de linha de comando dada. Ponto de entrada publico desta unidade."""
    global option
    option = opcao
    met = {'-f':  ('°C','m/s'), '-F':  ('°F','mph'), '-c':  ('°C','m/s'), '-C':  ('°F','mph')}
    parseJSONforCITY(response, cidade, met)
