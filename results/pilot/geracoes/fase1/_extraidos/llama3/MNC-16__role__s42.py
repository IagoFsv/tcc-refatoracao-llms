"""Previsao do tempo de uma cidade, impressa no terminal.

Ponto de entrada publico: executar(response, cidade, opcao). Nao altere o
nome nem a assinatura dessa funcao; o restante do arquivo pode ser
reorganizado livremente.
"""

option = '-c'

def parse_json_for_city(response, cidade):
    """Prints the weather forecast for the given city."""
    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}

    if option in ['-f', '-F']:
        print("5-day Forecast for " + cidade)
        for item in response['list']:
            date = item['dt_txt'][0:10]
            print(f"Date: {date}")
            print(f"Time: {item['dt_txt'][11:16]} Temperature: {item['main']['temp']} {met[option][0]} Weather: {item['weather'][0]['main']}")
            print("-------------------------------------------------------")
    else:
        print("-------------------------------------------------------")
        print("Current Weather for " + cidade)
        print(f"Temperature: {response['main']['temp']} {met[option][0]}")
        print(f"Wind Speed: {response['wind']['speed']} {met[option][1]}")
        print(f"Weather: {response['weather'][0]['main']}")
        print(f"Feels Like: {response['main']['feels_like']} {met[option][0]}")
        print(f"Humidity: {response['main']['humidity']}%")
        print(f"Minimum Temperature: {response['main']['temp_min']} {met[option][0]}")
        print(f"Maximum Temperature: {response['main']['temp_max']} {met[option][0]}")
        print("-------------------------------------------------------")


def executar(response, cidade, opcao):
    """Imprime o clima com a opcao de linha de comando dada. Ponto de entrada publico desta unidade."""
    global option
    option = opcao
    parse_json_for_city(response, cidade)
