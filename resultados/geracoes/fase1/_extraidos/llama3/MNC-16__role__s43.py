def print_weather(response, cidade, opcao):
    """Imprime o clima com a opcao de linha de comando dada."""
    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}
    print(f"5-day Forecast for {cidade}")
    day = ""
    for i in range(0, len(response['list'])):
        if day == response['list'][i]['dt_txt'][0:10]:
            print(f"Time: {response['list'][i]['dt_txt'][11:16]} Temperature: {str('%.1f' % (response['list'][i]['main']['temp']))} {met[opcao][0]} Weather: {response['list'][i]['weather'][0]['main']}")
        else:
            day = response['list'][i]['dt_txt'][0:10]
            print("-------------------------------------------------------")
            print(f"Date: {day}")
            print(f"Time: {response['list'][i]['dt_txt'][11:16]} Temperature: {str('%.1f' % (response['list'][i]['main']['temp']))} {met[opcao][0]} Weather: {response['list'][i]['weather'][0]['main']}")
    else:
        print("-------------------------------------------------------")
        print(f"Current Weather for {cidade}")
        if opcao in ['-f', '-F', '-c', '-C']:
            print(f"Temperature: {str('%.1f' % (response['main']['temp']))} {met[opcao][0]}")
            print(f"Wind Speed: {str('%.1f' % (response['wind']['speed']))} {met[opcao][1]}")
            print(f"Weather: {response['weather'][0]['main']}")
            print(f"Feels Like: {str('%.1f' % (response['main']['feels_like']))} {met[opcao][0]}")
            print(f"Humidity: {str(response['main']['humidity'])}%")
            print(f"Minimum Temperature: {str('%.1f' %  (response['main']['temp_min']))} {met[opcao][0]}")
            print(f"Maximum Temperature: {str('%.1f' %  (response['main']['temp_max']))} {met[opcao][0]}")
            print("-------------------------------------------------------")


def executar(response, cidade, opcao):
    """Imprime o clima com a opcao de linha de comando dada. Ponto de entrada publico desta unidade."""
    global option
    option = opcao
    print_weather(response, cidade, opcao)
