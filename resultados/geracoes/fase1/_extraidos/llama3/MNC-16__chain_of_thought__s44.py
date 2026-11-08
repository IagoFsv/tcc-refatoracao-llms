def parse_date_group(response, group):
    """Printa o conteúdo de um grupo de datas"""
    print("-------------------------------------------------------")
    print("Date: " + group['dt_txt'][0:10])
    print("Time: " + group['dt_txt'][11:16] + " Temperature: " + str('%.1f' % (group['main']['temp'])) + met[option][0] + " Weather: " + group['weather'][0]['main'])

def parse_current_weather(response):
    """Printa o clima atual"""
    print("-------------------------------------------------------")
    print("Current Weather for " + cidade)
    print("Temperature: " + str('%.1f' % (response['main']['temp'])) + met[option][0])
    print("Wind Speed: " + str('%.1f' % (response['wind']['speed'])) + met[option][1])
    print("Weather: " + response['weather'][0]['main'])
    print("Feels Like: " + str('%.1f' % (response['main']['feels_like'])) + met[option][0])
    print("Humidity: " + str(response['main']['humidity']) + "%")
    print("Minimum Temperature: " + str('%.1f' %  (response['main']['temp_min'])) + met[option][0])
    print("Maximum Temperature: " + str('%.1f' %  (response['main']['temp_max'])) + met[option][0])

def executar(response, cidade, opcao):
    """Imprime o clima com a opcao de linha de comando dada. Ponto de entrada publico desta unidade."""
    global option
    option = opcao
    if option in ['-f', '-F']:
        for group in response['list']:
            if group['dt_txt'][0:10] == day:
                print("Time: " + group['dt_txt'][11:16] + " Temperature: " + str('%.1f' % (group['main']['temp'])) + met[option][0] + " Weather: " + group['weather'][0]['main'])
            else:
                day = group['dt_txt'][0:10]
                parse_date_group(response, group)
    else:
        parse_current_weather(response)
