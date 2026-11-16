from termcolor import colored
from datetime import datetime


def get_current_date():
    """Get current date."""
    return datetime.now().strftime("%a, %d-%b-%y")


def format_section_title(title: str):
    """Format section title."""
    return colored(f"\n[*] {title}", "red", attrs=["bold"])


def format_weather_section(data):
    """Format weather section."""
    return (
        colored(
            f" - {data.get('current', {}).get('Time', 'N/A')} | Temp: {data.get('current', {}).get('Temp', 'N/A')} | Feels: {data.get('current', {}).get('Phrase', 'N/A')} | AQI (?)",
            "red",
        )
        + "\n"
        + colored(
            f" - RealFeel Sun: {data.get('current', {}).get('Realfeel sun', 'N/A')} | RealFeel Shade: {data.get('current', {}).get('Realfeel shade', 'N/A')} | UV Index: {data.get('current', {}).get('Max uv index', 'N/A')}",
            "blue",
        )
        + "\n"
        + colored(
            f" - Wind: {data.get('current', {}).get('Wind', ' N/A')[1:]} | Gusts: {data.get('current', {}).get('Wind gusts', 'N/A')} | Cloud Cover: {data.get('current', {}).get('Cloud cover', 'N/A')}",
            "green",
        )
        + "\n"
        + colored(
            f" - Dew Point: {data.get('current', {}).get('Dew point', 'N/A')} | Humidity: {data.get('current', {}).get('Humidity', 'N/A')} | Indoor Humidity: {data.get('current', {}).get('Indoor humidity', 'N/A')}",
            "cyan",
        )
        + "\n"
        + colored(
            f" - Visibility: {data.get('current', {}).get('Visibility', 'N/A')} | Pressure: {data.get('current', {}).get('Pressure', 'N/A')} | Ceiling: {data.get('current', {}).get('Cloud ceiling', 'N/A')}",
            "yellow",
        )
    )


def format_day_time_section(data):
    """Format day time forecast section."""
    return (
        format_section_title("DayTime Forecast")
        + colored(
            f" - Temp: {data.get('day', {}).get('Temp', 'N/A')} | Feels: {data.get('day', {}).get('Phrase', 'N/A')} | AQI (?)",
            "yellow",
        )
        + "\n"
        + colored(
            f" - UV Index: {data.get('day', {}).get('Max UV Index', 'N/A')} | Wind: {data.get('day', {}).get('Wind', 'N/A')} | Gusts: {data.get('day', {}).get('Wind Gusts', 'N/A')}",
            "green",
        )
        + "\n"
        + colored(
            f" - Cloud Cover: {data.get('day', {}).get('Cloud Cover', 'N/A')} | Rain: {data.get('day', {}).get('Rain', 'N/A')} | Thunder: {data.get('day', {}).get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )


def format_night_time_section(data):
    """Format night time forecast section."""
    return (
        format_section_title("NightTime Forecast")
        + colored(
            f" - Temp: {data.get('night', {}).get('Temp', 'N/A')} | Feels: {data.get('night', {}).get('Phrase', 'N/A')} | AQI (?)",
            "yellow",
        )
        + "\n"
        + colored(
            f" - UV Index: {data.get('night', {}).get('Max UV Index', 'N/A')} | Wind: {data.get('night', {}).get('Wind', 'N/A')} | Gusts: {data.get('night', {}).get('Wind Gusts', 'N/A')}",
            "green",
        )
        + "\n"
        + colored(
            f" - Cloud Cover: {data.get('night', {}).get('Cloud Cover', 'N/A')} | Rain: {data.get('night', {}).get('Rain', 'N/A')} | Thunder: {data.get('night', {}).get('Probability of Thunderstorms', 'N/A')}",
            "blue",
        )
    )


def format_forecast_section(data):
    """Format forecast for next 5 days section."""
    forecast = data.get("forecast", [])
    forecast_text = ""
    for i in range(5):
        forecast_text += (
            colored(
                f" -> {forecast[i+1].get('Date', 'N/A')} | {forecast[i+1].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[i+1].get('Temp', {}).get('min', 'N/A')}",
                "magenta",
            )
            + "\n"
            + colored(
                " " * 3
                + f"- Rain: {forecast[i+1].get('Rain', 'N/A')} | Hours of Rain: {forecast[i+1].get('Hours of Precipitation', 'N/A')} | Cloud Cover: {forecast[i+1].get('Cloud Cover', 'N/A')}",
                "green",
            )
            + "\n"
            + colored(
                " " * 3
                + f"- Wind: {forecast[i+1].get('Wind', ' N/A')[1:]} | Gusts: {forecast[i+1].get('Wind Gusts', 'N/A')} | Thunder: {forecast[i+1].get('Probability of Thunderstorms', 'N/A')}",
                "yellow",
            )
            + "\n"
        )
    return forecast_text


def format_powered_by_section(start_time: datetime):
    """Format powered by section."""
    return colored(
        "\n "
        + "-" * 17
        + f"{colored(f'Powered by AccuWeather ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}"
        + f"{colored('-'* 17, 'red')}",
        "green",
    )


def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    """Format the weather data to CLI response."""
    current_weather = format_weather_section(data)
    day_time_forecast = format_day_time_section(data)
    night_time_forecast = format_night_time_section(data)
    forecast = format_forecast_section(data)
    powered_by = format_powered_by_section(start_time)

    return (
        colored(
            f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
        + "\n"
        + current_weather
        + day_time_forecast
        + night_time_forecast
        + forecast
        + powered_by
    )


def executar(dados, cidade, codigo_pais):
    """Imprime o clima de dados, cronometrando a partir de agora. Ponto de entrada publico desta unidade."""
    return fmt_cli_resp(dados, cidade, codigo_pais, datetime.now())
