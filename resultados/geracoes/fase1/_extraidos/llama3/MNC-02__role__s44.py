import asyncio
from types import SimpleNamespace

import requests

class Embed:
    def __init__(self, **kwargs):
        self.title = kwargs.get("title")
        self.color = kwargs.get("color")
        self.thumbnail = None
        self.fields = []
        self.footer = None

    def set_thumbnail(self, *, url):
        self.thumbnail = url
        return self

    def add_field(self, *, name, value, inline=True):
        self.fields.append((str(name), str(value), inline))
        return self

    def set_footer(self, *, text=None, icon_url=None):
        self.footer = (text, icon_url)
        return self

discord = SimpleNamespace(Embed=Embed)

class ComandoSlash:
    def __init__(self, func):
        self.func = func

    async def invoke(self, *args, **kwargs):
        return await self.func(*args, **kwargs)

class SlashCommand:
    def slash(self, *, name=None, description=None, guild_ids=None, options=None, **kwargs):
        def wrapper(cmd):
            return ComandoSlash(cmd)
        return wrapper

slash = SlashCommand()

class Contexto:
    def __init__(self):
        self.author = SimpleNamespace(name="Ana", avatar_url="https://cdn.exemplo.com/ana.png")
        self.enviados = []

    async def send(self, content=None, *, embed=None):
        self.enviados.append(embed)

@slash.slash(name="weather",
             description="Weather for a specific location",
             options=[
               create_option(
                 name="location",
                 description="example: London",
                 option_type=3,
                 required=True
               )
             ])
async def weather(ctx, location):
    weather_api_key = get_weather_api_key()
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}')
    json_response = response.json()
    weather_data = parse_weather_data(json_response)
    embed = create_embed(weather_data)
    await ctx.send(embed=embed)

def get_weather_api_key():
    with open('./tokens/weather.txt', 'r') as file:
        return file.read()

def parse_weather_data(json_response):
    temp = round(json_response['main']['temp'] - 273.15)
    weather = json_response['weather'][0]['main']
    icon = json_response['weather'][0]['icon']
    wind = json_response['wind']['speed']
    humidity = json_response['main']['humidity']
    pressure = json_response['main']['pressure']
    cloud_cover = json_response['clouds']['all']
    city = json_response['name']
    country = json_response['sys']['country']
    return {
        'city': city,
        'country': country,
        'temp': temp,
        'weather': weather,
        'icon': icon,
        'wind': wind,
        'humidity': humidity,
        'pressure': pressure,
        'cloud_cover': cloud_cover
    }

def create_embed(weather_data):
    embed = discord.Embed(title=f"Weather in {weather_data['city']}, {weather_data['country']}", color=0x3f3f3f)
    embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{weather_data['icon']}@4x.png")
    embed.add_field(name="Temperature", value=f"{weather_data['temp']}°C", inline=True)
    embed.add_field(name="Weather", value=f"{weather_data['weather']}", inline=True)
    embed.add_field(name="Wind", value=f"{weather_data['wind']}m/s", inline=True)
    embed.add_field(name="Humidity", value=f"{weather_data['humidity']}%", inline=True)
    embed.add_field(name="Pressure", value=f"{weather_data['pressure']}hPa", inline=True)
    embed.add_field(name="Cloud Cover", value=f"{weather_data['cloud_cover']}%", inline=True)
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    return embed

def executar(local):
    ctx = Contexto()
    asyncio.run(weather.invoke(ctx, local))
    return ctx.enviados
