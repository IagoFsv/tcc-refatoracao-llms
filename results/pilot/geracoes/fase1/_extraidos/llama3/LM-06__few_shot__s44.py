def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def format_weather_data(data):
    """Format the weather data."""
    return {
        "Time": data.get("current", {}).get("Time", "N/A"),
        "Temp": data.get("current", {}).get("Temp", "N/A"),
        "Feels": data.get("current", {}).get("Phrase", "N/A"),
        "AQI": "?",
        "RealFeel Sun": data.get("current", {}).get("Realfeel sun", "N/A"),
        "RealFeel Shade": data.get("current", {}).get("Realfeel shade", "N/A"),
        "UV Index": data.get("current", {}).get("Max uv index", "N/A"),
        "Wind": data.get("current", {}).get("Wind", " N/A")[1:],
        "Gusts": data.get("current", {}).get("Wind gusts", "N/A"),
        "Cloud Cover": data.get("current", {}).get("Cloud cover", "N/A"),
        "Dew Point": data.get("current", {}).get("Dew point", "N/A"),
        "Humidity": data.get("current", {}).get("Humidity", "N/A"),
        "Indoor Humidity": data.get("current", {}).get("Indoor humidity", "N/A"),
        "Visibility": data.get("current", {}).get("Visibility", "N/A"),
        "Pressure": data.get("current", {}).get("Pressure", "N/A"),
        "Ceiling": data.get("current", {}).get("Cloud ceiling", "N/A"),
    }


def format_day_time_forecast(data):
    """Format the day time forecast."""
    return [
        {
            "Temp": data.get("day", {}).get("Temp", "N/A"),
            "Feels": data.get("day", {}).get("Phrase", "N/A"),
            "AQI": "?",
            "UV Index": data.get("day", {}).get("Max UV Index", "N/A"),
            "Wind": data.get("day", {}).get("Wind", "N/A"),
            "Gusts": data.get("day", {}).get("Wind Gusts", "N/A"),
            "Cloud Cover": data.get("day", {}).get("Cloud Cover", "N/A"),
            "Rain": data.get("day", {}).get("Rain", "N/A"),
            "Thunder": data.get("day", {}).get("Probability of Thunderstorms", "N/A"),
        }
    ]


def format_night_time_forecast(data):
    """Format the night time forecast."""
    return [
        {
            "Temp": data.get("night", {}).get("Temp", "N/A"),
            "Feels": data.get("night", {}).get("Phrase", "N/A"),
            "AQI": "?",
            "UV Index": data.get("night", {}).get("Max UV Index", "N/A"),
            "Wind": data.get("night", {}).get("Wind", "N/A"),
            "Gusts": data.get("night", {}).get("Wind Gusts", "N/A"),
            "Cloud Cover": data.get("night", {}).get("Cloud Cover", "N/A"),
            "Rain": data.get("night", {}).get("Rain", "N/A"),
            "Thunder": data.get("night", {}).get("Probability of Thunderstorms", "N/A"),
        }
    ]


def format_forecast(data):
    """Format the forecast for next 5 days."""
    return [
        {
            "Date": forecast.get("Date", "N/A"),
            "Temp": {
                "max": forecast.get("Temp", {}).get("max", "N/A"),
                "min": forecast.get("Temp", {}).get("min", "N/A"),
            },
            "Rain": forecast.get("Rain", "N/A"),
            "Hours of Precipitation": forecast.get("Hours of Precipitation", "N/A"),
            "Cloud Cover": forecast.get("Cloud Cover", "N/A"),
            "Wind": forecast.get("Wind", " N/A")[1:],
            "Gusts": forecast.get("Wind Gusts", "N/A"),
            "Probability of Thunderstorms": forecast.get("Probability of Thunderstorms", "N/A"),
        }
        for forecast in data.get("forecast", [])
    ]


def fmt_cli_resp(data, city, country_code, start_time):
    """Format the weather data to CLI response."""
    print(
        colored(
            f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    print(
        colored(
            format_weather_data(data),
            "red",
        )
    )
    print(
        colored(
            "[*] DayTime Forecast",
            "red",
            attrs=["bold"],
        )
    )
    print(
        colored(
            format_day_time_forecast(data),
            "yellow",
        )
    )
    print(
        colored(
            "[*] NightTime Forecast",
            "red",
            attrs=["bold"],
        )
    )
    print(
        colored(
            format_night_time_forecast(data),
            "blue",
        )
    )
    print(
        colored(
            "[*] Forecast for next 5 days",
            "red",
            attrs=["bold"],
        )
    )
    for forecast in format_forecast(data):
        print(
            colored(
                f" -> {forecast.get('Date', 'N/A')} | {forecast.get('Temp', {}).get('max', 'N/A')} >>>>> {forecast.get('Temp', {}).get('min', 'N/A')}",
                "magenta",
            )
        )
        print(
            colored(
                " " * 3
                + f"- Rain: {forecast.get('Rain', 'N/A')} | Hours of Rain: {forecast.get('Hours of Precipitation', 'N/A')} | Cloud Cover: {forecast.get('Cloud Cover', 'N/A')}",
                "green",
            )
        )
        print(
            colored(
                " " * 3
                + f"- Wind: {forecast.get('Wind', ' N/A')[1:]} | Gusts: {forecast.get('Wind Gusts', 'N/A')} | Thunder: {forecast.get('Probability of Thunderstorms', 'N/A')}",
                "yellow",
            )
        )
    print(
        colored(
            "\n "
            + "-" * 17
            + f"{colored(f'Powered by AccuWeather ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}"
            + f"{colored('-'* 17, 'red')}",
            "green",
        )
    )


def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    return fmt_cli_resp(dados, cidade, codigo_pais, datetime.now())
