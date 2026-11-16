from termcolor import colored
from datetime import datetime

def get_current_date():
    return datetime.now().strftime("%a, %d-%b-%y")

def fmt_cli_resp(data, city: str, country_code: str, start_time: datetime) -> str:
    print(
        colored(
            f"[*] Current Weather for {city.capitalize()}, {country_code.upper()} [{colored(get_current_date(), 'yellow')}{colored(']', 'green')}",
            "green",
            attrs=["bold"],
        )
    )
    format_and_print(data, 'current', 'Time', 'Temp', 'Feels', 'AQI (?)')
    format_and_print(data, 'current', 'Realfeel sun', 'Realfeel shade', 'UV Index', 'N/A')
    format_and_print(data, 'current', 'Wind', 'Wind gusts', 'Cloud Cover', 'N/A')
    format_and_print(data, 'current', 'Dew point', 'Humidity', 'Indoor Humidity', 'N/A')
    format_and_print(data, 'current', 'Visibility', 'Pressure', 'Ceiling', 'N/A')

    print(colored("\n[*] DayTime Forecast", "red", attrs=["bold"]))
    format_and_print(data, 'day', 'Temp', 'Phrase', 'AQI (?)')
    format_and_print(data, 'day', 'Max UV Index', 'Wind', 'Gusts', 'N/A')
    format_and_print(data, 'day', 'Cloud Cover', 'Rain', 'Probability of Thunderstorms', 'N/A')

    print(colored("\n[*] NightTime Forecast", "red", attrs=["bold"]))
    format_and_print(data, 'night', 'Temp', 'Phrase', 'AQI (?)')
    format_and_print(data, 'night', 'Max UV Index', 'Wind', 'Gusts', 'N/A')
    format_and_print(data, 'night', 'Cloud Cover', 'Rain', 'Probability of Thunderstorms', 'N/A')

    print(colored("\n[*] Forecast for next 5 days", "red", attrs=["bold"]))
    forecast = data.get("forecast", [])
    for i in range(5):
        print(
            colored(
                f" -> {forecast[i+1].get('Date', 'N/A')} | {forecast[i+1].get('Temp', {}).get('max', 'N/A')} >>>>> {forecast[i+1].get('Temp', {}).get('min', 'N/A')}",
                "magenta",
            )
        )
        format_and_print(forecast[i+1], 'Rain', 'N/A', 'Hours of Precipitation', 'N/A', 'Cloud Cover', 'N/A')
        format_and_print(forecast[i+1], 'Wind', ' N/A', 'Wind Gusts', 'N/A', 'Thunder', 'Probability of Thunderstorms', 'N/A')

    print(
        colored(
            "\n "
            + "-" * 17
            + f"{colored(f'Powered by AccuWeather ({round((datetime.now() - start_time).total_seconds(), 2)}s)', 'yellow')}"
            + f"{colored('-'* 17, 'red')}",
            "green",
        )
    )

def format_and_print(data, section, *keys):
    for key in keys:
        print(
            colored(
                f" - {data.get(section, {}).get(key, 'N/A')}",
                "red" if section == 'current' else "yellow" if section == 'day' or section == 'night' else "green" if section == 'forecast' else "magenta"
            )
        )

def executar(dados, cidade, codigo_pais):
    return fmt_cli_resp(dados, cidade, codigo_pais, datetime.now())
