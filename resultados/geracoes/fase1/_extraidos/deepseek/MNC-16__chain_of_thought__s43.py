option = '-c'

def parse_current_weather(response, CITY, met):
    print("-------------------------------------------------------")
    print("Current Weather for " + CITY)
    print("Temperature: " + str('%.1f' % (response['main']['temp'])) + met[option][0])
    print("Wind Speed: " + str('%.1f' % (response['wind']['speed'])) + met[option][1])
    print("Weather: " + response['weather'][0]['main'])

def parse_forecast(response, CITY, met):
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

def parseJSONforCITY(response, CITY):
    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}

    if option == '-f' or option == '-F':
        parse_forecast(response, CITY, met)
    else:
        parse_current_weather(response, CITY, met)

def executar(response, cidade, opcao):
    global option
    option = opcao
    parseJSONforCITY(response, cidade)
