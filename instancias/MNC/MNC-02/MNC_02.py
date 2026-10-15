"""Comando de clima de um bot de chat: consulta a previsao e responde com um cartao.

Ponto de entrada publico: executar(local). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import asyncio
from types import SimpleNamespace

import requests


class Embed:
    """Cartao de mensagem, com a mesma interface de discord.Embed."""

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
    """Comando registrado; invoke repassa os argumentos para a corrotina."""

    def __init__(self, func):
        self.func = func

    async def invoke(self, *args, **kwargs):
        return await self.func(*args, **kwargs)


class SlashCommand:
    """Registro de comandos de barra; slash() devolve o comando registrado."""

    def slash(self, *, name=None, description=None, guild_ids=None, options=None, **kwargs):
        def wrapper(cmd):
            return ComandoSlash(cmd)
        return wrapper


def create_option(name, description, option_type, required, choices=None):
    return {"name": name, "description": description, "type": option_type,
            "required": required, "choices": choices or []}


slash = SlashCommand()


class Contexto:
    """Contexto do comando: quem pediu e as mensagens enviadas de volta."""

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
  # Request:
  # Open the file ./tokens/weather.txt and read the token and set it as weather_api_key
  with open('./tokens/weather.txt', 'r') as file:
    weather_api_key = file.read()
  response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}')
  json_response = response.json()
  temp = json_response['main']['temp']
  temp = round(temp - 273.15)
  weather = json_response['weather'][0]['main']
  icon = json_response['weather'][0]['icon']
  wind = json_response['wind']['speed']
  humidity = json_response['main']['humidity']
  pressure = json_response['main']['pressure']
  cloud_cover = json_response['clouds']['all']
  city = json_response['name']
  country = json_response['sys']['country']

  # Message
  embed=discord.Embed(title=f"Weather in {city}, {country}", color=0x3f3f3f)
  embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}@4x.png")
  embed.add_field(name="Temperature", value=f"{temp}°C", inline=True)
  embed.add_field(name="Weather", value=f"{weather}", inline=True)
  embed.add_field(name="Wind", value=f"{wind}m/s", inline=True)
  embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
  embed.add_field(name="Pressure", value=f"{pressure}hPa", inline=True)
  embed.add_field(name="Cloud Cover", value=f"{cloud_cover}%", inline=True)
  embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)


def executar(local):
    """Roda o comando para o local e devolve os cartoes enviados. Ponto de entrada publico desta unidade."""
    ctx = Contexto()
    asyncio.run(weather.invoke(ctx, local))
    return ctx.enviados
