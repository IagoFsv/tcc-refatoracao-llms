def create_weather_message(temp, weather, wind, humidity, pressure, cloud_cover, city, country, icon):
    embed = discord.Embed(title=f"Weather in {city}, {country}", color=0x3f3f3f)
    embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}@4x.png")
    embed.add_field(name="Temperature", value=f"{temp}°C", inline=True)
    embed.add_field(name="Weather", value=f"{weather}", inline=True)
    embed.add_field(name="Wind", value=f"{wind}m/s", inline=True)
    embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
    embed.add_field(name="Pressure", value=f"{pressure}hPa", inline=True)
    embed.add_field(name="Cloud Cover", value=f"{cloud_cover}%", inline=True)
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    return embed

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
    # ...
    weather_data = {
        "temp": round(json_response['main']['temp'] - 273.15),
        "weather": json_response['weather'][0]['main'],
        "icon": json_response['weather'][0]['icon'],
        "wind": json_response['wind']['speed'],
        "humidity": json_response['main']['humidity'],
        "pressure": json_response['main']['pressure'],
        "cloud_cover": json_response['clouds']['all'],
        "city": json_response['name'],
        "country": json_response['sys']['country']
    }
    embed = create_weather_message(**weather_data)
    await ctx.send(embed=embed)
