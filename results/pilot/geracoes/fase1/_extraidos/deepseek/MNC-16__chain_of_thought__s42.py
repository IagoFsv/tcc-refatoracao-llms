"""Previsao do tempo de uma cidade, impressa no terminal.

Ponto de entrada publico: executar(response, cidade, opcao). Nao altere o
nome nem a assinatura dessa funcao; o restante do arquivo pode ser
reorganizado livremente.
"""

def print_current_weather(response, CITY, option):
    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}
    print("-------------------------------------------------------")
    print("Current Weather for " + CITY)
    print("Temperature: " + str('%.1f' % (response['main']['temp'])) + met[option][0])
    print("Wind Speed: " + str('%.1f' % (response['wind']['speed'])) + met[option][1])
    print("Weather: " + response['weather'][0]['main'])
    print("Feels Like: " + str('%.1f' % (response['main']['feels_like'])) + met[option][0])
    print("Humidity: " + str(response['main']['humidity']) + "%")
    print("Minimum Temperature: " + str('%.1f' % (response['main']['temp_min'])) + met[option][0])
    print("Maximum Temperature: " + str('%.1f' % (response['main']['temp_max'])) + met[option][0])
    print("-------------------------------------------------------")

def print_forecast(response, CITY, option):
    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}
    print("5-day Forecast for " + CITY)
    day = ""
    for i in range(0, len(response['list'])):
        if day == response['list'][i]['dt_txt'][0:10]:
            print("Time: " + response['list'][i]['dt_txt'][11:16] + " Temperature: " + str('%.1f' % (response['list'][i]['main']['temp'])) + met[option][0] + " Weather: " + response['list'][i]['weather'][0]['main'])
        else:
            day = response['list'][i]['dt_txt'][0:10]
            print("-------------------------------------------------------")
            print("Date: " + day)
            print("Time: " + response['list'][i]['dt_txt'][11:16] + " Temperature: " + str('%.1f' % (response['list'][i]['main']['temp'])) + met[option][0] + " Weather: " + response['list'][i]['weather'][0]['main'])

def executar(response, cidade, opcao):
    """Imprime o clima com a opcao de linha de comando dada. Ponto de entrada publico desta unidade."""
    if opcao == '-f' or opcao == '-F':
        print_forecast(response, cidade, opcao)
    else:
        print_current_weather(response, cidade, opcao)
