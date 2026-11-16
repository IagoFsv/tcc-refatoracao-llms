from dataclasses import dataclass, field
from typing import List

@dataclass
class WeatherResponse:
    temp: float
    weather: str
    icon: str
    wind: float
    humidity: int
    pressure: int
    cloud_cover: int
    city: str
    country: str

@dataclass
class Embed:
    title: str
    color: int
    thumbnail: str
    fields: List[tuple]
    footer: tuple

@dataclass
class Context:
    author: str
    avatar_url: str
    enviados: List[Embed] = field(default_factory=list)

@dataclass
class WeatherOption:
    name: str
    description: str
    option_type: int
    required: bool
    choices: List[str] = field(default_factory=list)

async def weather(location: str):
    # Request:
    weather_api_key = open('./tokens/weather.txt', 'r').read()
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}')
    json_response = response.json()
    weather_response = WeatherResponse(
        temp=round(json_response['main']['temp'] - 273.15),
        weather=json_response['weather'][0]['main'],
        icon=json_response['weather'][0]['icon'],
        wind=json_response['wind']['speed'],
        humidity=json_response['main']['humidity'],
        pressure=json_response['main']['pressure'],
        cloud_cover=json_response['clouds']['all'],
        city=json_response['name'],
        country=json_response['sys']['country']
    )

    # Message
    embed = Embed(
        title=f"Weather in {weather_response.city}, {weather_response.country}",
        color=0x3f3f3f,
        thumbnail=f"http://openweathermap.org/img/wn/{weather_response.icon}@4x.png",
        fields=[
            ("Temperature", f"{weather_response.temp}°C", True),
            ("Weather", f"{weather_response.weather}", True),
            ("Wind", f"{weather_response.wind}m/s", True),
            ("Humidity", f"{weather_response.humidity}%", True),
            ("Pressure", f"{weather_response.pressure}hPa", True),
            ("Cloud Cover", f"{weather_response.cloud_cover}%", True)
        ],
        footer=(f"Requested by {location}", None)
    )
    return embed

def executar(local):
    """Roda o comando para o local e devolve os cartoes enviados. Ponto de entrada publico desta unidade."""
    ctx = Context()
    embed = weather(local)
    ctx.enviados.append(embed)
    return ctx.enviados
