"""Weather command of a chat bot: queries the forecast and replies with a card.

Public entry point: run(location). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import asyncio
from types import SimpleNamespace

import requests
from dataclasses import dataclass

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


class Weather:
    """Weather data with all relevant fields."""

    def __init__(self, temp, weather, icon, wind, humidity, pressure, cloud_cover, city, country):
        self.temp = temp
        self.weather = weather
        self.icon = icon
        self.wind = wind
        self.humidity = humidity
        self.pressure = pressure
        self.cloud_cover = cloud_cover
        self.city = city
        self.country = country


class Context:
    """Command context: who asked and the messages sent back."""

    def __init__(self):
        self.author = SimpleNamespace(name="Ana", avatar_url="https://cdn.example.com/ana.png")
        self.sent = []

    async def send(self, content=None, *, embed=None):
        self.sent.append(embed)


@dataclass
class CommandOption:
    name: str
    description: str
    type: int
    required: bool
    choices: list[str] = None


slash = SimpleNamespace()


def create_option(name, description, option_type, required, choices=None):
    return CommandOption(name, description, option_type, required, choices or [])


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
    with open('./tokens/weather.txt', 'r') as file:
        weather_api_key = file.read()
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}')
    json_response = response.json()
    temp = round(json_response['main']['temp'] - 273.15)
    weather = json_response['weather'][0]['main']
    icon = json_response['weather'][0]['icon']
    wind = json_response['wind']['speed']
    humidity = json_response['main']['humidity']
    pressure = json_response['main']['pressure']
    cloud_cover = json_response['clouds']['all']
    city = json_response['name']
    country = json_response['sys']['country']

    # Weather data
    weather_data = Weather(temp, weather, icon, wind, humidity, pressure, cloud_cover, city, country)

    # Message
    embed = discord.Embed(title=f"Weather in {city}, {country}", color=0x3f3f3f)
    embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}@4x.png")
    embed.add_field(name="Temperature", value=f"{temp}°C", inline=True)
    embed.add_field(name="Weather", value=f"{weather}", inline=True)
    embed.add_field(name="Wind", value=f"{wind}m/s", inline=True)
    embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
    embed.add_field(name="Pressure", value=f"{pressure}hPa", inline=True)
    embed.add_field(name="Cloud Cover", value=f"{cloud_cover}%", inline=True)
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


def run(location):
    """Runs the command for the location and returns the cards sent. Public entry point of this unit."""
    ctx = Context()
    asyncio.run(weather.invoke(ctx, location))
    return ctx.sent
