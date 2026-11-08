from dataclasses import dataclass, field
from typing import List

@dataclass
class Temperatura:
    valor: float
    unidade: str

@dataclass
class Vento:
    velocidade: float
    unidade: str

@dataclass
class Condicao:
    principal: str
    detalhes: str

@dataclass
class Previsao:
    data: str
    hora: str
    temperatura: Temperatura
    vento: Vento
    condicao: Condicao

@dataclass
class Resposta:
    main: Previsao
    wind: Vento
    weather: List[Condicao]

def parseJSONforCITY(response: Resposta, cidade: str):
    met = {'-f': ('°C','m/s'), '-F': ('°F','mph'), '-c': ('°C','m/s'), '-C': ('°F','mph')}
    
    if option == '-f' or option == '-F':
        print("5-day Forecast for " + cidade)
        day = ""
        for i in range(0, len(response.main)):
            if day == response.main[i].data[0:10]:
                print("Time: " + response.main[i].hora + " Temperature: " + str('%.1f' % (response.main[i].temperatura.valor)) + met[option][0] + " Weather: " + response.main[i].condicao.principal)
            else:
                day = response.main[i].data[0:10]
                print("-------------------------------------------------------")
                print("Date: " + day)
                print("Time: " + response.main[i].hora + " Temperature: " + str('%.1f' % (response.main[i].temperatura.valor)) + met[option][0] + " Weather: " + response.main[i].condicao.principal)             
    else:
        print("-------------------------------------------------------")
        print("Current Weather for " + cidade)
        print("Temperature: " + str('%.1f' % (response.main.temperatura.valor)) + met[option][0])
        print("Wind Speed: " + str('%.1f' % (response.wind.velocidade)) + met[option][1])
        print("Weather: " + response.weather[0].principal)
        print("Feels Like: " + str('%.1f' % (response.main.feels_like)) + met[option][0])
        print("Humidity: " + str(response.main.humidity) + "%")
        print("Minimum Temperature: " + str('%.1f' %  (response.main.temp_min)) + met[option][0])
        print("Maximum Temperature: " + str('%.1f' %  (response.main.temp_max)) + met[option][0])
        print("-------------------------------------------------------")

def executar(response: Resposta, cidade: str, opcao: str):
    global option
    option = opcao
    parseJSONforCITY(response, cidade)
