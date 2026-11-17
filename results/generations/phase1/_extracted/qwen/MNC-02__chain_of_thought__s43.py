"""Weather command of a chat bot: queries the forecast and replies with a card.

Public entry point: run(location). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import asyncio
from types import SimpleNamespace

import requests


class Embed:
    """Message card, with the same interface as discord.Embed."""

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


class CommandObject:
    """Registered command; invoke passes the arguments on to the coroutine."""

    def __init__(self, func):
        self.func = func

    async def invoke(self, *args, **kwargs):
        return await self.func(*args, **kwargs)


class SlashCommand:
    """Registry of slash commands; slash() returns the registered command."""

    def slash(self, *, name=None, description=None, guild_ids=None, options=None, **kwargs):
        def wrapper(cmd):
            return CommandObject(cmd)
        return wrapper


def create_option(name, description, option_type, required, choices=None):
    return {"name": name, "description": description, "type": option_type,
            "required": required, "choices": choices or []}


slash = SlashCommand()


class Context:
    """Command context: who asked and the messages sent back."""

    def __init__(self):
        self.author = SimpleNamespace(name="Ana", avatar_url="https://cdn.example.com/ana.png")
        self.sent = []

    async def send(self, content=None, *, embed=None):
        self.sent.append(embed)


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
  
  # Extract data using helper functions
  temp = get_temperature(json_response)
  weather = get_weather(json_response)
  icon = get_icon(json_response)
  wind = get_wind(json_response)
  humidity = get_humidity(json_response)
  pressure = get_pressure(json_response)
  cloud_cover = get_cloud_cover(json_response)
  city = get_city(json_response)
  country = get_country(json_response)

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


def get_temperature(json_response):
    return round(json_response['main']['temp'] - 273.15)


def get_weather(json_response):
    return json_response['weather'][0]['main']


def get_icon(json_response):
    return json_response['weather'][0]['icon']


def get_wind(json_response):
    return json_response['wind']['speed']


def get_humidity(json_response):
    return json_response['main']['humidity']


def get_pressure(json_response):
    return json_response['main']['pressure']


def get_cloud_cover(json_response):
    return json_response['clouds']['all']


def get_city(json_response):
    return json_response['name']


def get_country(json_response):
    return json_response['sys']['country']


def run(location):
    """Runs the command for the location and returns the cards sent. Public entry point of this unit."""
    ctx = Context()
    asyncio.run(weather.invoke(ctx, location))
    return ctx.sent
