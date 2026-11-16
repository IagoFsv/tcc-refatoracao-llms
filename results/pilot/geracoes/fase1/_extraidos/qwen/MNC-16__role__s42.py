option = '-c'

def parseJSONforCITY(response, CITY, opcao):
    '''
    print only for key = main, key = wind speed and key = weather[main] in a pretty format
    '''

    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}
    format_temp = lambda temp, unit: f"{temp:.1f}{unit}"

    if opcao == '-f' or opcao == '-F':
        print("5-day Forecast for " + CITY)
        day = ""
        for item in response['list']:
            if day == item['dt_txt'][0:10]:
                print(f"Time: {item['dt_txt'][11:16]} Temperature: {format_temp(item['main']['temp'], met[opcao][0])} Weather: {item['weather'][0]['main']}")
            else:
                day = item['dt_txt'][0:10]
                print("-------------------------------------------------------")
                print(f"Date: {day}")
                print(f"Time: {item['dt_txt'][11:16]} Temperature: {format_temp(item['main']['temp'], met[opcao][0])} Weather: {item['weather'][0]['main']}")
    else:
        print("-------------------------------------------------------")
        print(f"Current Weather for {CITY}")
        print(f"Temperature: {format_temp(response['main']['temp'], met[opcao][0])}")
        print(f"Wind Speed: {format_temp(response['wind']['speed'], met[opcao][1])}")
        print(f"Weather: {response['weather'][0]['main']}")
        print(f"Feels Like: {format_temp(response['main']['feels_like'], met[opcao][0])}")
        print(f"Humidity: {response['main']['humidity']}%")
        print(f"Minimum Temperature: {format_temp(response['main']['temp_min'], met[opcao][0])}")
        print(f"Maximum Temperature: {format_temp(response['main']['temp_max'], met[opcao][0])}")
        print("-------------------------------------------------------")


def executar(response, cidade, opcao):
    """Imprime o clima com a opcao de linha de comando dada. Ponto de entrada publico desta unidade."""
    parseJSONforCITY(response, cidade, opcao)
