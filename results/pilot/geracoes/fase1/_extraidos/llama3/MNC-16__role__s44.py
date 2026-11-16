"""Previsao do tempo de uma cidade, impressa no terminal.

Ponto de entrada publico: executar(response, cidade, opcao). Nao altere o
nome nem a assinatura dessa funcao; o restante do arquivo pode ser
reorganizado livremente.
"""

option = '-c'

def parse_json_for_city(response, cidade):
    for key, value in response.items():
        if key == 'main':
            print("Current Weather for " + cidade)
            print("Temperature: " + str('%.1f' % (value['temp'])) + met[option][0])
            print("Wind Speed: " + str('%.1f' % (value['temp'])) + met[option][1])
            print("Weather: " + value['weather'][0]['main'])
        elif key == 'wind':
            print("Wind Speed: " + str('%.1f' % (value['speed'])) + met[option][1])
        elif key == 'weather':
            for weather in value:
                print("Weather: " + weather['main'])

def executar(response, cidade, opcao):
    """Imprime o clima com a opcao de linha de comando dada. Ponto de entrada publico desta unidade."""
    global option
    option = opcao
    if opcao in ['-f', '-F', '-c', '-C']:
        for i in range(0, len(response['list'])):
            if i > 0 and response['list'][i]['dt_txt'][0:10] != response['list'][i-1]['dt_txt'][0:10]:
                print("-------------------------------------------------------")
                print("Date: " + response['list'][i]['dt_txt'][0:10])
            print("Time: " + response['list'][i]['dt_txt'][11:16] + " Temperature: " + str('%.1f' % (response['list'][i]['main']['temp'])) + met[option][0] + " Weather: " + response['list'][i]['weather'][0]['main'])
    else:
        print("-------------------------------------------------------")
        print("5-day Forecast for " + cidade)
        for i in range(0, len(response['list'])):
            print("Time: " + response['list'][i]['dt_txt'][11:16] + " Temperature: " + str('%.1f' % (response['list'][i]['main']['temp'])) + met[option][0] + " Weather: " + response['list'][i]['weather'][0]['main'])
