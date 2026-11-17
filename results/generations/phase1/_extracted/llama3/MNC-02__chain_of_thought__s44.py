def weather(ctx, location):
  # Request:
  # Open the file ./tokens/weather.txt and read the token and set it as weather_api_key
  with open('./tokens/weather.txt', 'r') as file:
    weather_api_key = file.read()
  response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}')
  json_response = response.json()

  # Extract weather data
  weather_data = {
    'temp': json_response['main']['temp'],
    'weather': json_response['weather'][0],
    'wind': json_response['wind'],
    'humidity': json_response['main']['humidity'],
    'pressure': json_response['main']['pressure'],
    'cloud_cover': json_response['clouds']['all'],
    'city': json_response['name'],
    'country': json_response['sys']['country']
  }

  # Message
  embed = discord.Embed(title=f"Weather in {weather_data['city']}, {weather_data['country']}", color=0x3f3f3f)
  embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{weather_data['weather']['icon']}@4x.png")
  embed.add_field(name="Temperature", value=f"{weather_data['temp']}°C", inline=True)
  embed.add_field(name="Weather", value=f"{weather_data['weather']['main']}", inline=True)
  embed.add_field(name="Wind", value=f"{weather_data['wind']['speed']}m/s", inline=True)
  embed.add_field(name="Humidity", value=f"{weather_data['humidity']}%", inline=True)
  embed.add_field(name="Pressure", value=f"{weather_data['pressure']}hPa", inline=True)
  embed.add_field(name="Cloud Cover", value=f"{weather_data['cloud_cover']}%", inline=True)
  embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
  await ctx.send(embed=embed)
