class WeatherInfo:
    """Classe para armazenar as informações do clima."""

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

def create_weather_info(json_response):
    """Função para criar um objeto WeatherInfo a partir de um JSON de resposta da API OpenWeather."""
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
    return WeatherInfo(temp, weather, icon, wind, humidity, pressure, cloud_cover, city, country)

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
    weather_info = create_weather_info(json_response)

    # Message
    embed = discord.Embed(title=f"Weather in  {weather_info.city},  {weather_info.country}", color=0x3f3f3f)
    embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{weather_info.icon}@4x.png")
    embed.add_field(name="Temperature", value=f"{weather_info.temp}°C", inline=True)
    embed.add_field(name="Weather", value=f"{weather_info.weather}", inline=True)
    embed.add_field(name="Wind", value=f"{weather_info.wind}m/s", inline=True)
    embed.add_field(name="Humidity", value=f"{weather_info.humidity}%", inline=True)
    embed.add_field(name="Pressure", value=f"{weather_info.pressure}hPa", inline=True)
    embed.add_field(name="Cloud Cover", value=f"{weather_info.cloud_cover}%", inline=True)
    embed.set_footer(text=f"Requested by  {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
