def parseJSONforCITY(response, CITY, option):
    met = {'-f': ('°C', 'm/s'), '-F': ('°F', 'mph'), '-c': ('°C', 'm/s'), '-C': ('°F', 'mph')}
    print_units = met[option]

    if option == '-f' or option == '-F':
        print("5-day Forecast for " + CITY)
        day = ""
        for i in range(0, len(response['list'])):
            if day == response['list'][i]['dt_txt'][0:10]:
                print("Time: " + response['list'][i]['dt_txt'][11:16] + " Temperature: " + str('%.1f' % (response['list'][i]['main']['temp'])) + print_units[0] + " Weather: " + response['list'][i]['weather'][0]['main'])
            else:
                day = response['list'][i]['dt_txt'][0:10]
                print("-------------------------------------------------------")
                print("Date: " + day)
                print("Time: " + response['list'][i]['dt_txt'][11:16] + " Temperature: " + str('%.1f' % (response['list'][i]['main']['temp'])) + print_units[0] + " Weather: " + response['list'][i]['weather'][0]['main'])

    else:
        print("-------------------------------------------------------")
        print("Current Weather for " + CITY)
        print("Temperature: " + str('%.1f' % (response['main']['temp'])) + print_units[0])
        print("Wind Speed: " + str('%.1f' % (response['wind']['speed'])) + print_units[1])
        print("Weather: " + response['weather'][0]['main'])
        print("Feels Like: " + str('%.1f' % (response['main']['feels_like'])) + print_units[0])
        print("Humidity: " + str(response['main']['humidity']) + "%")
        print("Minimum Temperature: " + str('%.1f' % (response['main']['temp_min'])) + print_units[0])
        print("Maximum Temperature: " + str('%.1f' % (response['main']['temp_max'])) + print_units[0])
        print("-------------------------------------------------------")

def executar(response, cidade, opcao):
    parseJSONforCITY(response, cidade, opcao)
