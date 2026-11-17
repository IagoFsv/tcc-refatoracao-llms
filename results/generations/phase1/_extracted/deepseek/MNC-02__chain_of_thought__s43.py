class WeatherData:
    def __init__(self, data):
        self.data = data

    def get_temperature(self):
        temp = self.data['main']['temp']
        return round(temp - 273.15)

    def get_weather(self):
        return self.data['weather'][0]['main']

    def get_icon(self):
        return self.data['weather'][0]['icon']

    def get_wind(self):
        return self.data['wind']['speed']

    def get_humidity(self):
        return self.data['main']['humidity']

    def get_pressure(self):
        return self.data['main']['pressure']

    def get_cloud_cover(self):
        return self.data['clouds']['all']

    def get_city(self):
        return self.data['name']

    def get_country(self):
        return self.data['sys']['country']


class Embed:
    # ... rest of the code remains the same


class CommandObject:
    # ... rest of the code remains the same


class SlashCommand:
    # ... rest of the code remains the same


class Context:
    # ... rest of the code remains the same


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
    with open('./tokens/weather.txt', 'r') as file:
        weather_api_key = file.read()
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}')
    json_response = response.json()
    data = WeatherData(json_response)

    embed = discord.Embed(title=f"Weather in {data.get_city()}, {data.get_country()}", color=0x3f3f3f)
    embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{data.get_icon()}@4x.png")
    embed.add_field(name="Temperature", value=f"{data.get_temperature()}°C", inline=True)
    embed.add_field(name="Weather", value=f"{data.get_weather()}", inline=True)
    embed.add_field(name="Wind", value=f"{data.get_wind()}m/s", inline=True)
    embed.add_field(name="Humidity", value=f"{data.get_humidity()}%", inline=True)
    embed.add_field(name="Pressure", value=f"{data.get_pressure()}hPa", inline=True)
    embed.add_field(name="Cloud Cover", value=f"{data.get_cloud_cover()}%", inline=True)
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


def run(location):
    ctx = Context()
    asyncio.run(weather.invoke(ctx, location))
    return ctx.sent
